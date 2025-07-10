import random
import string
from datetime import date, timedelta
from django.utils import timezone

import uuid

import pytest
from playwright.sync_api import expect


# def test_invite_participant(apps, as_admin):

#     Experiment = apps.backend.get_model('experiments', 'Experiment')
#     Location = apps.backend.get_model('experiments', 'Location')
#     apps.backend.load('leader.json')
#     location = Location.objects.create(name="Test Lab")
#     page = as_admin
#     page.goto(f"{apps.backend.url}/experiments/2/invite/")
#     page.check('input[name="participants[]"]');
#     page.click('#submit')
#     success_alert = page.locator(".alert")
#     expect(success_alert).to_have_text('Successfully invited participants!')
#     assert success_alert.is_visible()














# def test_cancel_appointment_from_email(apps, adult_participant, mailbox, link_from_mail, page):
#     apps.backend.load('admin')
#     Experiment = apps.backend.get_model('experiments', 'Experiment')
#     User = apps.backend.get_model('main', 'User')
#     Appointment = apps.backend.get_model('experiments', 'Appointment')

#     from utils.appointment_mail import send_appointment_mail, prepare_appointment_mail

#     leader = User.objects.first()
#     experiment = Experiment.objects.create(duration=10, session_duration=20, name='Memory Task')
#     experiment.leaders.add(leader)
#     experiment.save()

#     start = timezone.now()
#     appointment = Appointment.objects.create(
#         experiment=experiment,
#         participant=adult_participant,
#         leader=leader,
#         start=start,
#     )

#     send_appointment_mail(appointment, prepare_appointment_mail(appointment))

#     page.goto(link_from_mail(adult_participant.email))

#     appointment.refresh_from_db()
#     assert appointment.outcome == Appointment.Outcome.CANCELED

#     try:
#         mail = mailbox(leader.email)
#         assert len(mail) == 1
#         text = mail[0].get_payload()[0].get_payload()
#         assert adult_participant.name not in text
#         assert 'canceled' in text.lower()
#     finally:
#         appointment.delete()


# def test_adult_appointment_shows_in_overview(apps, adult_participant, page, login_as):
#     apps.backend.load('admin')
#     Experiment = apps.backend.get_model("experiments", "Experiment")
#     User = apps.backend.get_model("main", "User")
#     Appointment = apps.backend.get_model("experiments", "Appointment")

#     experiment = Experiment.objects.create(duration=10, session_duration=20, name='Memory Test')
#     leader = User.objects.first()
#     start = timezone.now()

#     experiment.leaders.add(leader)
#     experiment.save()

#     appointment = Appointment.objects.create(
#         experiment=experiment,
#         participant=adult_participant,
#         leader=leader,
#         start=start,
#     )

#     login_as(adult_participant.email)

#     try:
#         expect(page.get_by_text('Appointments')).to_be_visible()
#         expect(page.get_by_text('Memory Test')).to_be_visible()
#         expect(page.get_by_text(leader.name)).to_be_visible()
#     finally:
#         appointment.delete()


# def test_past_appointment_not_in_adult_overview(apps, adult_participant, page, login_as):
#     apps.backend.load('admin')
#     Experiment = apps.backend.get_model("experiments", "Experiment")
#     User = apps.backend.get_model("main", "User")
#     Appointment = apps.backend.get_model("experiments", "Appointment")

#     leader = User.objects.first()
#     experiment = Experiment.objects.create(
#         duration=10,
#         session_duration=20,
#         name='Past Experiment'
#     )
#     experiment.leaders.add(leader)
#     experiment.save()

#     start = timezone.now() - timedelta(days=30)
#     appointment = Appointment.objects.create(
#         experiment=experiment,
#         participant=adult_participant,
#         leader=leader,
#         start=start,
#     )

#     login_as(adult_participant.email)

#     try:
#         expect(page.get_by_text('Appointments')).to_be_visible()
#         expect(page.get_by_text('Past Experiment')).not_to_be_visible()
#         expect(page.get_by_text(leader.name)).not_to_be_visible()
#     finally:
#         appointment.delete()
