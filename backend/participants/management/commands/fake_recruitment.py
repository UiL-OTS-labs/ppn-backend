import random
from datetime import datetime, timedelta
from typing import List

from django.core.management.base import BaseCommand, CommandError
from faker import Faker

from participants.models import Participant

DEFAULT_PREFIX = "F_"

fake = Faker()


LANGUAGES = ["Nederlands", "Engels", "Frans", "Spaans", "Duits", "Arabisch"]


def simulate_recruitment(number: int, date: datetime, name_prefix=DEFAULT_PREFIX):
    """Simulate a recruitment this will add participant to the database. It's
    useful for generating participants to give some body to the database.

    The name_prefix gives a unlikely name for a participant in order to remove it
    from the database.

    Keyword arguments:
    :param int number: the number of participants to create
    :param datetime date: The date around which the participants are born
    :param days_spread: The number of days around the data the children are born
    :param str name_prefix: A prefix to prepend to the participant name
    """
    for i in range(number):
        name = DEFAULT_PREFIX + fake.name()
        email = "generated-{}@gen.mars".format(random.randint(int(1e6), int(1e7)))
        birth_date = fake.date_of_birth()
        sex = random.choice(["M", "F", "PNTA"])

        pp = Participant.objects.create(
            name=name,
            sex=sex,
            birth_date=birth_date,
            email=email,
            phonenumber=fake.phone_number(),
            email_subscription=random.choice([True, False]),
            social_status=random.choice(Participant.SOCIAL_STATUS),
            language=random.choice(LANGUAGES),
        )
        pp.save()
        pp.created = date
        pp.save()


def _get_simulated_participants(prefix) -> List[Participant]:
    """
    The encrypted fields are a bit unfriendly with Model.objects.filter()
    This touches the fields in order to decrypt the values.
    This method finds the fake pp's in order to delete them
    """
    pps = Participant.objects.all()
    return [pp for pp in pps if pp.name.startswith(prefix)]


def remove_simulated_participants(prefix: str = DEFAULT_PREFIX):
    """This function attempts to delete participants created with
    simulate_recruitment
    """
    rm_pps = _get_simulated_participants(prefix)
    for pp in rm_pps:
        pp.data.delete()
        pp.delete()


def _positive_int(value):
    intval = int(value)
    if intval < 0:
        raise CommandError(message="Expected value larger than 0")
    return intval


class Command(BaseCommand):
    """
    Allow manage.py to generate participants for debug purposes.
    """

    help = "Generate participants for testing purposes, NOT for production"

    def add_arguments(self, parser):
        parser.add_argument("year", help="The year of the test recruitment", type=int)
        parser.add_argument(
            "month",
            help="The month of the test recruitment",
            choices=list(range(1, 13)),
            type=int,
        )
        parser.add_argument(
            "--day", help="The month of the test recruitment", type=int, default=1
        )
        parser.add_argument(
            "-n",
            "--number",
            help="The number of participant that are recruited",
            type=_positive_int,
            default=100,
        )

    def handle(self, *args, **options):
        """Validates provided arguments"""
        year = options["year"]
        month = options["month"]
        day = options["day"]
        number = options["number"]

        date = datetime(year=year, month=month, day=day)

        simulate_recruitment(number, date)
