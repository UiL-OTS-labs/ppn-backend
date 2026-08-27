from datetime import datetime, timedelta

from freezegun import freeze_time
from django.test import TestCase
from django.utils.timezone import get_current_timezone

from auditlog.models import LogEntry
from participants.models import Participant
from .common import _create_dummy_user, _create_thresholds, _create_experiment, \
    _create_participant
from experiments.models import Appointment, Invitation, TimeSlot
from ..utils.common import get_thresholds_model
from ..utils.participants import delete_participant, \
    get_participants_with_appointments, \
    get_participants_without_appointments


@freeze_time("2026-05-01")
class ParticipantTests(TestCase):
    databases = ['default', 'auditlog']

    def setUp(self) -> None:
        _create_thresholds()
        self.participants = []
        self.experiments = []

        for days_offset in range(5, 16):
            dt = datetime.now(tz=get_current_timezone()) - \
                 timedelta(days=days_offset)
            self.participants.append(
                _create_participant(
                    "offset_used: {}".format(days_offset),
                    dt
                )
            )
            self.experiments.append(
                _create_experiment([dt])
            )

    def test_no_appointments(self):
        num = get_participants_without_appointments()

        # Should have offsets 10 to 15 for a total of 6 participants
        self.assertEqual(len(num), 6)

        # Check with a different threshold
        thresholds = get_thresholds_model()
        thresholds.participants_without_appointment = 11
        thresholds.save()

        num = get_participants_without_appointments()

        # Should have offsets 11 to 15 for a total of 5 participants
        self.assertEqual(len(num), 5)

    def test_all_appointments(self):
        for participant, experiment in zip(self.participants, self.experiments):
            timeslot = experiment.timeslot_set.first()
            app = Appointment.objects.create(
                timeslot=timeslot,
                participant=participant,
                experiment=experiment,
            )
            # It checks on creation_date now, so we just copy the TS' datetime
            app.creation_date = app.timeslot.datetime
            app.save()

        num = get_participants_with_appointments()

        # Should have offsets 10 to 15 for a total of 6 participants
        self.assertEqual(len(num), 6)

        # Check which participants are shown
        shown_pks = [p.pk for p, _, _ in num]
        for participant in self.participants[:5]:  # offsets 5-9, below threshold
            self.assertNotIn(participant.pk, shown_pks)
        for participant in self.participants[5:]:  # offsets 10-15, above threshold
            self.assertIn(participant.pk, shown_pks)

        # Check with a different threshold
        thresholds = get_thresholds_model()
        thresholds.participants_with_appointment = 11
        thresholds.save()
        get_thresholds_model.cache_clear()

        num = get_participants_with_appointments()

        # Should have offsets 11 to 15 for a total of 5 participants
        self.assertEqual(len(num), 5)

        # Check which participants are shown after threshold change
        shown_pks = [p.pk for p, _, _ in num]
        for participant in self.participants[:6]:  # offsets 5-10, below threshold
            self.assertNotIn(participant.pk, shown_pks)
        for participant in self.participants[6:]:  # offsets 11-15, above threshold
            self.assertIn(participant.pk, shown_pks)

        # Test that code looks at timeslot datetime, not appointment creation_date
        # Participant with old timeslot (5 years ago) but recent creation_date (today)
        # Should be shown because timeslot is above threshold of 3 years
        old_participant = _create_participant(
            "old_timeslot",
            datetime.now(tz=get_current_timezone()) - timedelta(days=365*10)
        )
        old_experiment = _create_experiment([
            datetime.now(tz=get_current_timezone()) - timedelta(days=365*5)  # timeslot 5 jaar geleden
        ])
        timeslot = old_experiment.timeslot_set.first()
        app = Appointment.objects.create(
            timeslot=timeslot,
            participant=old_participant,
            experiment=old_experiment,
        )
        app.creation_date = datetime.now(tz=get_current_timezone())  # creation_date vandaag!
        app.save()

        thresholds = get_thresholds_model()
        thresholds.participants_with_appointment = 365*3  # threshold 3 jaar
        thresholds.save()
        get_thresholds_model.cache_clear()

        num = get_participants_with_appointments()
        shown_pks = [p.pk for p, _, _ in num]

        # Should be shown because timeslot was 5 years ago (above threshold of 3 years)
        self.assertIn(old_participant.pk, shown_pks)

    def test_participant_deletion(self):
        # Pick negative indexes, as we want participants that are above the
        # threshold (which are located in the last half of the list)
        participant_1 = self.participants[-1]
        participant_2 = self.participants[-2]

        timeslot = self.experiments[0].timeslot_set.first()
        Appointment.objects.create(
            timeslot=timeslot,
            participant=participant_1,
            experiment=self.experiments[0],
        )

        # This should refuse to delete, as there is an appointment
        deletion_1 = delete_participant(participant_1, _create_dummy_user())
        self.assertFalse(deletion_1)
        self.assertEqual(Participant.objects.count(), len(self.participants))

        # This should return true and delete the participant
        deletion_2 = delete_participant(participant_2, _create_dummy_user())
        self.assertTrue(deletion_2)
        self.assertEqual(Participant.objects.count(), len(self.participants)-1)

        # Check if the auditlog logged anything
        self.assertEqual(LogEntry.objects.count(), 1)
