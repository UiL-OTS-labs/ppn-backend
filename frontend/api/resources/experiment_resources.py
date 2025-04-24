from cdh.rest import client as rest


class Location(rest.Resource):
    """
    This resources describes a test location. route_url can be null if no
    routing info is present.
    """
    id = rest.IntegerField()

    name = rest.TextField()

    route_url = rest.TextField(blank=True, null=True)


class Experiment(rest.Resource):
    class Meta:
        path = '/api/experiments/{pk}/'
        path_variables = ['pk']

    id = rest.IntegerField()

    name = rest.TextField()

    duration = rest.TextField()

    compensation = rest.TextField()

    task_description = rest.TextField(blank=True)

    additional_instructions = rest.TextField(blank=True)

    open = rest.BoolField()

    public = rest.BoolField()

    participants_visible = rest.BoolField()

    location = rest.ResourceField(Location, null=True, blank=True)

    leader = rest.ResourceField('Leader')  # We cannot import this, as this
    # will cause a circular import

    additional_leaders = rest.CollectionField('Leaders')

    excluded_experiments = rest.CollectionField('OpenExperiments')

    defaultcriteria = rest.ResourceField(
        'DefaultCriteria',
        null=True,
        blank=True
    )

    specific_criteria = rest.CollectionField('ExperimentCriteria')

    use_timeslots = rest.BoolField()

    timeslots = rest.CollectionField('InlineTimeSlots')

    default_max_places = rest.IntegerField()

    def __str__(self):
        return self.name

    def is_leader(self, user) -> bool:
        if self.leader.api_user and self.leader.api_user.id == user.id:
            return True

        for leader in self.additional_leaders:
            if leader.api_user.id == user.id:
                return True

        return False

    def n_timeslots(self):
        return sum([t.max_places for t in self.timeslots])

    def display_additional_leaders(self):
        return ", ".join([leader.name for leader in self.additional_leaders])


class LeaderExperiment(Experiment):
    class Meta:
        path = '/api/leader_experiments/{pk}/'
        path_variables = ['pk']

    timeslots = rest.CollectionField('LeaderInlineTimeSlots')

    appointments = rest.CollectionField('LeaderTimeSlotAppointments')

    @property
    def n_participants(self):
        return len(self.appointments)


class SwitchExperimentOpen(rest.Resource):
    class Meta:
        path = '/api/experiment/{experiment}/switch_open/'
        supported_operations = [rest.Operations.get_over_post]
        path_variables = ['experiment']

    success = rest.BoolField()

    open = rest.BoolField()


class ReminderParticipants(rest.Resource):
    class Meta:
        path = '/api/experiment/{experiment}/remind_participants/'
        supported_operations = [rest.Operations.put]
        path_variables = ['experiment']

    appointments = rest.CollectionField(rest.IntegerCollection)


class LeaderExperiments(rest.ResourceCollection):
    class Meta:
        resource = LeaderExperiment
        path = '/api/leader_experiments/'


class OpenExperiments(rest.ResourceCollection):
    class Meta:
        resource = Experiment
        path = '/api/experiments/'


class RegistrationCriterion(rest.Resource):

    name = rest.TextField()

    value = rest.TextField()


class RegistrationCriteria(rest.ResourceCollection):
    class Meta:
        resource = RegistrationCriterion


class ExperimentRegistrationResponse(rest.Resource):

    success = rest.BoolField()

    recoverable = rest.BoolField()

    messages = rest.CollectionField(rest.StringCollection)


class ExperimentRegistration(rest.Resource):
    class Meta:
        path = '/api/experiment/{experiment}/register/'
        supported_operations = [rest.Operations.put]
        path_variables = ['experiment']
        default_return_resource = ExperimentRegistrationResponse

    full = rest.BoolField(
        default=True,
    )

    name = rest.TextField(
        blank=True,
        null=True,
    )

    email = rest.TextField(
        blank=True,
        null=True,
    )

    phone = rest.TextField(
        blank=True,
        null=True,
    )

    birth_date = rest.DateField(
        blank=True,
        null=True,
    )

    multilingual = rest.TextField(
        blank=True,
        null=True,
    )

    language = rest.TextField(
        blank=True,
        null=True,
    )

    sex = rest.TextField(
        blank=True,
        null=True,
    )

    handedness = rest.TextField(
        blank=True,
        null=True,
    )

    dyslexic = rest.TextField(
        blank=True,
        null=True,
    )

    social_status = rest.TextField(
        blank=True,
        null=True,
    )

    specific_criteria = rest.CollectionField(
        RegistrationCriteria
    )

    timeslot = rest.IntegerField()

    mailinglist = rest.BoolField(
        default=False
    )
