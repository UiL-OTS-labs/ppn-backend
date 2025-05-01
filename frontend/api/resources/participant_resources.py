from datetime import datetime

from cdh.rest import client as rest
from .generic_resources import SuccessResponse


#
# Mailing list related resources
#

class MailinglistSubscribe(rest.Resource):
    """
    This resources is used to subscribe a 'new' participant to the mailing list
    """

    class Meta:
        path = '/api/participant/subscribe_mailinglist/'
        supported_operations = [rest.Operations.put]
        default_return_resource = SuccessResponse

    email = rest.TextField()

    language = rest.TextField()

    multilingual = rest.TextField()

    dyslexic = rest.BoolField()


class ValidateMailinglistTokenResponse(rest.Resource):
    """
    This resources is used as the response resources for ValidateMailinglistToken.

    Email will be filled in if success == True, to be used to display it.
    """

    success = rest.BoolField()

    email = rest.TextField(null=True, blank=True)


class ValidateMailinglistToken(rest.Resource):
    """
    This resources is used to validate unsubscribe-from-mailinglist tokens, will
    return the ValidateMailinglistTokenResponse resources
    """

    class Meta:
        path = '/api/participant/validate_mailinglist_token/'
        supported_operations = [rest.Operations.put]
        default_return_resource = ValidateMailinglistTokenResponse

    token = rest.TextField()


class UnsubscribeFromMailinglist(rest.Resource):
    """
    This resources is used to unsubscribe a participant from the mailing list.
    The participant is identified by the token.

    You can use ValidateMailinglistToken to validate the token beforehand
    """

    class Meta:
        path = '/api/participant/unsubscribe_from_mailinglist/'
        supported_operations = [rest.Operations.put]
        default_return_resource = SuccessResponse

    token = rest.TextField()


#
# Appointment related resources
#

class SendCancelToken(rest.Resource):
    """
    This resources is used to request a appointment cancel token for a given
    email. For security purposes this token is sent by the backend through
    email.

    It uses the generic SuccessResponse Resource as the default response.
    """

    class Meta:
        path = '/api/participant/send_cancel_token/'
        supported_operations = [rest.Operations.put]
        default_return_resource = SuccessResponse

    email = rest.TextField()


class Appointment(rest.Resource):
    """
    This resources represents an appointment for a participant(!), it can
    retrieve them when the pk is known. NOTE: this will error if no user
    header is present, so it will only work when a participant is logged in!

    It can also delete them using the delete method.
    To retrieve all appointments for a participant, use the Appointments
    collection. (below)
    """

    class Meta:
        path = '/api/participant/appointments/{id}/'
        path_variables = ['id']
        supported_operations = [rest.Operations.get, rest.Operations.delete]

    id = rest.IntegerField()

    creation_date = rest.DateTimeField()

    timeslot = rest.ResourceField('TimeSlot', null=True, blank=True)

    experiment = rest.ResourceField('Experiment')

    @property
    def can_cancel(self) -> bool:
        if self.timeslot is None:
            return True

        # If the appointment is in the future, one can cancel
        return self.timeslot.datetime > datetime.now(
            tz=self.timeslot.datetime.tzinfo
        )


class Appointments(rest.ResourceCollection):
    """
    A collection of all appointments for a participant(!).  NOTE: this will
    error if no user header is present, so it will only work when a
    participant is logged in!
    """

    class Meta:
        path = '/api/participant/appointments/'
        supported_operations = [rest.Operations.get]
        resource = Appointment


#
# Register fields resources
#

class RequiredRegistrationFields(rest.Resource):
    """
    This resources can be used to get the required register fields for a given
    experiment.
    NOTE: This only works (and makes sense) when a participant is logged in
    """

    class Meta:
        path = '/api/participant/get_required_fields/{experiment}/'
        path_variables = ['experiment']

        supported_operations = [rest.Operations.get]

    fields = rest.CollectionField(
        rest.StringCollection
    )


#
# Participant resources
#


class Participant(rest.Resource):
    """
    Describes a participant. It does not have it's own endpoint, so it can
    only be used in other resources as a field or in collections.
    """
    id = rest.IntegerField()

    name = rest.TextField()

    email = rest.TextField()

    phonenumber = rest.TextField(
        null=True,
        blank=True,
    )

    language = rest.TextField()

    multilingual = rest.BoolField()

    birth_date = rest.DateField(
        null=True,
        blank=True,
    )

    handedness = rest.TextField(
        null=True,
        blank=True,
    )

    sex = rest.TextField(
        null=True,
        blank=True,
    )

    social_status = rest.TextField(
        null=True,
        blank=True,
    )

    email_subscription = rest.BoolField()

    def get_social_status_display(self):
        if self.social_status == 'S':
            return 'Student'

        return 'Geen student'
