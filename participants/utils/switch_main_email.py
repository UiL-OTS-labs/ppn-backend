from typing import Union

from participants.models import Participant, SecondaryEmail


def switch_main_email(
        participant: Participant,
        new_email: Union[str, SecondaryEmail]
) -> None:
    """
    This function switches the main email of a participant with one of it's
    secondary emails. The old secondary email object is used to store the
    previous main email.

    :param participant: A participant object
    :param new_email: An email string that corresponds to a secondary email
                      or the SE directly
    :type new_email: str | SecondaryEmail
    :return: Nothing
    """
    def to_lower(string: str) -> str:
        return str(string).lower()

    # Lookup the SE instance if we got an email string
    if isinstance(new_email, str):
        # Get the secondary email that now houses the new main email
        secondary_emails = participant.secondaryemail_set.all()
        try:
            secondary_email = next(
                iter([x for x in secondary_emails if to_lower(x.email) ==
                      to_lower(new_email)])
            )
        except StopIteration:
            # Should not happen, but if it happens it can ruin one's day so we
            # need to have a fallback
            secondary_email = SecondaryEmail()
            secondary_email.participant = participant
    else:
        secondary_email = new_email
        new_email = new_email.email

    # If we don't actually have a primary email, just delete the SE
    if participant.email is None:
        # But only if we didn't just create it
        if secondary_email.pk:
            secondary_email.delete()
    else:
        # Set the old main email as this object's email address
        secondary_email.email = participant.email
        secondary_email.save()

    # Set the new email (same as the original value of the secondary email
    # above) as the main email
    participant.email = new_email
    participant.save()
