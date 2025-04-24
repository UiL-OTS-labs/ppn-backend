from typing import List

from api.resources.generic_resources import SuccessResponse
from api.resources.participant_resources import Participant
from cdh.core.utils import enumerate_to

from cdh.rest import client as rest
from babel.dates import format_datetime
from django.utils.translation import get_language


class TimeSlotAppointment(rest.Resource):
    """
    Different from the participant appointment, as this one is a child of
    a timeslot. The participant appointment has a timeslot resources as a
    child.
    """
    id = rest.IntegerField()

    creation_date = rest.DateTimeField()


class LeaderTimeSlotAppointment(TimeSlotAppointment):
    """
    Different from the normal TimeSlotAppointment, as this one includes
    info about the participant.
    """
    id = rest.IntegerField()

    creation_date = rest.DateTimeField()

    participant = rest.ResourceField(Participant)


class TimeSlotAppointments(rest.ResourceCollection):
    class Meta:
        resource = TimeSlotAppointment


class LeaderTimeSlotAppointments(rest.ResourceCollection):
    class Meta:
        resource = LeaderTimeSlotAppointment


class InlineTimeSlot(rest.Resource):

    id = rest.IntegerField()

    datetime = rest.DateTimeField()

    max_places = rest.IntegerField()

    free_places = rest.IntegerField()

    appointments = rest.CollectionField(TimeSlotAppointments)

    @property
    def places(self) -> list:
        """Returns a list of places with a corresponding participant (if any)"""
        appointments = self.appointments or []
        return [{
            'n':           n,
            'appointment': appointment
        } for n, appointment in enumerate_to(appointments,
                                             self.max_places, 1)]

    @property
    def takes_places_tuple(self) -> List[tuple]:
        return [(x['n'], x['appointment']) for x in self.places if
                x['appointment']]

    def has_free_places(self) -> bool:
        return self.free_places != 0

    @property
    def free_places(self) -> int:
        if self.appointments is None:
            return 0

        return self.max_places - len(self.appointments)

    def __str__(self):
        places_str = "uur"
        if self.free_places > 1:
            places_str = "uur ({} plekken resterend)".format(self.free_places)

        # Behold! The function chain FROM HELL! (Sorry)
        return format_datetime(
            self.datetime,
            'EEEE, dd-MM-YYYY, HH:mm {}',
            locale=get_language()
        ).format(
            places_str
        ).capitalize()


class LeaderInlineTimeSlot(InlineTimeSlot):

    appointments = rest.CollectionField(LeaderTimeSlotAppointments)


class LeaderInlineTimeSlots(rest.ResourceCollection):
    class Meta:
        resource = LeaderInlineTimeSlot


class InlineTimeSlots(rest.ResourceCollection):
    class Meta:
        resource = InlineTimeSlot


class TimeSlot(rest.Resource):
    class Meta:
        path = 'api/experiment/{experiment}/add_time_slot/'
        path_variables = ['experiment']
        supported_operations = [rest.Operations.put]
        default_return_resource = SuccessResponse
        default_send_as_json = True

    experiment = rest.IntegerField()

    datetime = rest.DateTimeField()

    max_places = rest.IntegerField()


class DeleteTimeSlots(rest.Resource):
    class Meta:
        path = 'api/experiment/{experiment}/delete_time_slots/'
        path_variables = ['experiment']
        supported_operations = [rest.Operations.put]
        default_return_resource = SuccessResponse
        default_send_as_json = True

    experiment = rest.IntegerField()

    to_delete = rest.CollectionField(rest.StringCollection)


class DeleteAppointment(rest.Resource):
    class Meta:
        path = 'api/experiment/{experiment}/delete_appointment/'
        path_variables = ['experiment']
        supported_operation = [rest.Operations.put]
        default_return_resource = SuccessResponse
        default_send_as_json = True

    experiment = rest.IntegerField()

    to_delete = rest.IntegerField()
