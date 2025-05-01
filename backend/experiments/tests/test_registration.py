import datetime

from api.auth.models import ApiUser
from api.utils.make_appointment import register_participant
from django.test import TestCase
from experiments.models import Experiment
from experiments.models.criteria_models import Criterion
from freezegun import freeze_time
from leaders.models import Leader
from main.models import User
from participants.models import Participant


class RegistrationTests(TestCase):
    def setUp(self):
        admin = User.objects.create(is_supreme_admin=True)
        self.pp = Participant(email="foo@bar.com", dyslexic=False, language="nl")
        leader_user = ApiUser.objects.create(email="leader@example.com")
        leader = Leader.objects.create(api_user=leader_user)
        self.exp = Experiment.objects.create(
            leader=leader, default_max_places=10, use_timeslots=False
        )

    def test_new_participant(self):
        success, _, messages = register_participant(
            dict(email=self.pp.email, specific_criteria=[], language="nl"), self.exp
        )
        assert success, messages

    def test_new_participant_specific_criteria(self):
        criterion = Criterion.objects.create(name_form="test_crit", values="yes,no")
        self.exp.experimentcriterion_set.create(
            criterion=criterion, correct_value="yes"
        )
        self.exp.save()
        specific_criteria = [dict(name="test_crit", value="0")]
        success, _, messages = register_participant(
            dict(
                email=self.pp.email, specific_criteria=specific_criteria, language="nl"
            ),
            self.exp,
        )
        assert success, messages

    @freeze_time("2017-12-31")
    def test_participant_age_at_time_of_appointment(self):
        self.pp.birth_date = datetime.date(2000, 1, 1)
        self.pp.save()
        self.exp.defaultcriteria.min_age = 18
        self.exp.use_timeslots = False
        self.exp.save()

        # first test that experiment with no time slots should fail
        success, _, messages = register_participant(
            dict(email=self.pp.email, specific_criteria=[], language="nl"), self.exp
        )
        assert not success

        # then test that experiment with time slots should succeed
        # but only when the participant is old enough
        self.exp.use_timeslots = True
        self.exp.save()
        slot_ok = self.exp.timeslot_set.create(max_places=1, datetime=datetime.datetime(2018, 1, 1, 10, 0))
        slot_bad = self.exp.timeslot_set.create(max_places=1, datetime=datetime.datetime(2017, 12, 31, 10, 0))

        success, _, messages = register_participant(
            dict(
                timeslot=slot_bad.pk,
                email=self.pp.email,
                specific_criteria=[],
                language="nl"), self.exp
        )
        assert not success

        success, _, messages = register_participant(
            dict(
                timeslot=slot_ok.pk,
                email=self.pp.email,
                specific_criteria=[],
                language="nl"), self.exp
        )
        assert success, messages
