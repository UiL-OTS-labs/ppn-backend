import string
import pprint
from datetime import datetime
import random

from dateutil.relativedelta import relativedelta
from django.test import TestCase
from pytz import timezone

from . import _get_or_create_leader, _get_or_create_location
from experiments.models import Experiment, Criterion, ExperimentCriterion, TimeSlot
from experiments.utils.exclusion import get_eligible_participants_for_experiment
from participants.models import Participant, CriterionAnswer



def make_participant(**kwargs):
    if 'dyslexic' not in kwargs:
        kwargs['dyslexic'] = False
    return Participant.objects.create(
        email=''.join(random.choices(string.ascii_lowercase, k=10)) + '@example.org',
        email_subscription=True,
        **kwargs
    )

class ExclusionTests(TestCase):
    def setUp(self):
        self.experiment = Experiment.objects.create(
            name='test',
            leader=_get_or_create_leader(),
            location=_get_or_create_location(),
        )
        self.experiment.defaultcriteria.language = 'I'
        self.experiment.defaultcriteria.multilingual = 'I'
        self.experiment.defaultcriteria.save()

        self.excluded_experiment = Experiment.objects.create(
            name='excluded',
            leader=_get_or_create_leader(),
            location=_get_or_create_location(),
        )

        self.time_slot = TimeSlot.objects.create(
            experiment=self.excluded_experiment,
            datetime=datetime.now(tz=timezone('UTC')),
            max_places=9000,
        )

        self.criterion = Criterion.objects.create(
            name_form='test',
            name_natural='test',
            values='yes,no',
        )

        self.dt_18 = datetime.now() - relativedelta(years=18)
        self.dt_20 = datetime.now() - relativedelta(years=20)
        self.dt_30 = datetime.now() - relativedelta(years=30)

    def format_pp(self, pp):
        return pprint.pformat(
            {field.name: field.value_from_object(pp) for field in pp._meta.concrete_fields}
        )

    def should_include(self, pp):
        pps = get_eligible_participants_for_experiment(self.experiment)
        if pp not in pps:
            raise AssertionError("Participant not included: \n" + self.format_pp(pp))

    def should_exclude(self, pp):
        pps = get_eligible_participants_for_experiment(self.experiment)
        if pp in pps:
            raise AssertionError("Participant not excluded: \n" + self.format_pp(pp))

    def test_exclude_default(self):
        """Exclude only dyslectics (the default)"""
        self.should_include(make_participant(dyslexic=False))
        self.should_exclude(make_participant(dyslexic=True))

    def test_exclude_non_dyslectics(self):
        """Exclude non dyslectics"""
        # Override the default value for language
        self.experiment.defaultcriteria.dyslexia = 'Y'

        self.should_include(make_participant(dyslexic=True))
        self.should_exclude(make_participant(dyslexic=False))

    def test_exclude_min_age(self):
        self.experiment.defaultcriteria.min_age = 19

        self.should_include(make_participant(birth_date=self.dt_30))
        self.should_include(make_participant(birth_date=self.dt_20))
        self.should_exclude(make_participant(birth_date=self.dt_18))

    def test_exclude_max_age(self):
        self.experiment.defaultcriteria.max_age = 25

        self.should_include(make_participant(birth_date=self.dt_18))
        self.should_include(make_participant(birth_date=self.dt_20))
        self.should_exclude(make_participant(birth_date=self.dt_30))

    def test_exclude_min_max_age(self):
        self.experiment.defaultcriteria.min_age = 19
        self.experiment.defaultcriteria.max_age = 25

        self.should_include(make_participant(birth_date=None))
        self.should_include(make_participant(birth_date=self.dt_20))
        self.should_exclude(make_participant(birth_date=self.dt_18))
        self.should_exclude(make_participant(birth_date=self.dt_30))

    def test_exclude_right_handed(self):
        self.experiment.defaultcriteria.handedness = 'L'

        self.should_include(make_participant(handedness='L'))
        self.should_exclude(make_participant(handedness='R'))

    def test_exclude_left_handed(self):
        self.experiment.defaultcriteria.handedness = 'R'

        self.should_include(make_participant(handedness='R'))
        self.should_exclude(make_participant(handedness='L'))

    def test_exclude_multilinguals(self):
        self.experiment.defaultcriteria.multilingual = 'N'

        self.should_include(make_participant(multilingual=False))
        self.should_exclude(make_participant(multilingual=True))

    def test_exclude_monolinguals(self):
        self.experiment.defaultcriteria.multilingual = 'Y'

        self.should_include(make_participant(multilingual=True))
        self.should_exclude(make_participant(multilingual=False))

    def test_exclude_elvish(self):
        self.experiment.defaultcriteria.language = 'nl'

        self.should_include(make_participant(language='nl'))
        self.should_exclude(make_participant(language='elvish'))

    def test_exclude_dutch(self):
        self.experiment.defaultcriteria.language = 'elvish'

        self.should_exclude(make_participant(language='nl'))
        self.should_include(make_participant(language='elvish'))

    def test_exclude_males(self):
        self.experiment.defaultcriteria.sex = 'F'

        self.should_exclude(make_participant(sex='M'))
        self.should_include(make_participant(sex='F'))
        self.should_include(make_participant(sex=None))

    def test_exclude_females(self):
        self.experiment.defaultcriteria.sex = 'M'

        self.should_exclude(make_participant(sex='F'))
        self.should_include(make_participant(sex='M'))
        self.should_include(make_participant(sex=None))

    def test_exclude_students(self):
        self.experiment.defaultcriteria.social_status = 'O'

        self.should_exclude(make_participant(social_status='S'))
        self.should_include(make_participant(social_status='O'))
        self.should_include(make_participant(social_status=None))

    def test_exclude_non_students(self):
        self.experiment.defaultcriteria.social_status = 'S'

        self.should_exclude(make_participant(social_status='O'))
        self.should_include(make_participant(social_status='S'))
        self.should_include(make_participant(social_status=None))

    def test_specific_criteria_exclusion(self):
        ExperimentCriterion.objects.create(
            experiment=self.experiment,
            criterion=self.criterion,
            correct_value='yes'
        )

        pp = make_participant()
        CriterionAnswer.objects.create(participant=pp, criterion=self.criterion, answer='yes')
        self.should_include(pp)

        pp2 = make_participant()
        CriterionAnswer.objects.create(participant=pp2, criterion=self.criterion, answer='no')
        self.should_exclude(pp2)

    def test_experiment_exclusion(self):
        self.experiment.excluded_experiments.add(self.excluded_experiment)

        pp = make_participant()
        self.excluded_experiment.appointments.create(participant=pp)

        self.should_exclude(pp)
        self.should_include(make_participant())

    def test_exclude_already_subscribed(self):
        pp = make_participant()
        self.experiment.appointments.create(participant=pp)

        self.should_exclude(pp)
        self.should_include(make_participant())
