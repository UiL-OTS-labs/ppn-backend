from datetime import datetime

from pytz import timezone

from api.resources import TimeSlot
from api.resources.timeslot_resources import DeleteTimeSlots, DeleteAppointment
from cdh.rest.client import StringCollection

_TIMESLOT_KEY_PREFIX = len("timeslot_")
_TIMESLOT_KEY_POSTFIX = len("[]")


def now() -> datetime:
    """This function returns a datetime object, set to the last minute that is
    a multiple of 5. Intended for a default value for a timeslot's datetime
    field.
    """
    datetime_now = datetime.now(tz=timezone('Europe/Amsterdam'))

    # Makes sure the minutes is a multiple of 5, by rounding down to the nearest
    minute = datetime_now.minute - (datetime_now.minute % 5)

    # We set tzinfo to 0 because it causes inconvenient output
    return datetime_now.replace(minute=minute, second=0, microsecond=0,
                                tzinfo=None)


def add_timeslot(data: dict) -> bool:
    """Does a put request with a newly created TimeSlot resources. Returns the
    API's indication if it worked.
    """
    time_slot = TimeSlot()
    time_slot.experiment = data.get('experiment')
    time_slot.datetime = data.get('datetime')
    time_slot.max_places = data.get('max_places')

    response = time_slot.put()

    return response.success


def delete_timeslot(experiment_pk, timeslot_pk) -> bool:
    to_delete = [
        "{}_1".format(timeslot_pk)
    ]
    return _delete_timeslots(experiment_pk, to_delete)


def delete_timeslots(experiment_pk, post_data) -> bool:
    to_delete = []
    for key in post_data.keys():
        if key.startswith('timeslot_'):
            timeslot_pk = int(key[_TIMESLOT_KEY_PREFIX:-_TIMESLOT_KEY_POSTFIX])

            values = post_data.getlist(key)

            to_delete.append(
                "{}_{}".format(
                    timeslot_pk,
                    len(values)
                )
            )

    return _delete_timeslots(experiment_pk, to_delete)


def _delete_timeslots(experiment_pk, to_delete) -> bool:
    delete_order = DeleteTimeSlots()
    delete_order.experiment = experiment_pk
    delete_order.to_delete = StringCollection(to_delete)

    response = delete_order.put()

    return response.success


def unsubscribe_participant(experiment_pk, appointment_pk):
    delete_order = DeleteAppointment()
    delete_order.experiment = experiment_pk
    delete_order.to_delete = appointment_pk

    response = delete_order.put()

    return response.success
