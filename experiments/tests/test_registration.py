from unittest import skip
from api.auth.models import ApiUser
from api.utils.make_appointment import register_participant

from django.test import TestCase

from experiments.models import Experiment
from experiments.models.criteria_models import Criterion
from leaders.models import Leader
from main.models import User
from participants.models import Participant


class RegistrationTests(TestCase):
    def setUp(self):
        admin = User.objects.create(is_supreme_admin=True)
        self.pp = Participant(
            email='foo@bar.com',
            dyslexic=False,
            language='nl'
        )
        leader_user = ApiUser.objects.create(email='leader@example.com')
        leader = Leader.objects.create(api_user=leader_user)
        self.exp = Experiment.objects.create(leader=leader, default_max_places=10, use_timeslots=False)

    def test_new_participant(self):
        success, _, messages = register_participant(dict(email=self.pp.email, specific_criteria=[]), self.exp)
        assert success, messages

    def test_new_participant_specific_criteria(self):
        criterion = Criterion.objects.create(name_form='test_crit', values='yes,no')
        self.exp.experimentcriterion_set.create(criterion=criterion, correct_value='no')
        self.exp.save()
        specific_criteria = [dict(name='test_crit', value='0')]
        success, _, messages = register_participant(dict(email=self.pp.email, specific_criteria=specific_criteria),
                                                    self.exp)
        assert success, messages
