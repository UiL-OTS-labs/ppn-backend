import csv
from collections.abc import Iterable
from io import StringIO

from .mailinglist_unsubscribe import get_mailinglist_unsubscribe_token, \
    get_mailinglist_unsubscribe_url
from .merge_participants import merge_participants

from ..models import Participant

def participants_csv(pps: Iterable[Participant]):
    """returns CSV formatted participants in a manner that's compatible with
    Django's StreamingHttpResponse"""
    io = StringIO()
    writer = csv.DictWriter(io, fieldnames=['id', 'name', 'email', 'secondary_email',
                                            'sex', 'language', 'multilingual', 'dyslexic',
                                            'created'])
    writer.writeheader()
    yield io.getvalue()

    for pp in pps:
        io.truncate(0)
        io.seek(0)
        writer.writerow({
                'id': pp.pk,
                'name': pp.name,
                'email': pp.email,
                'secondary_email': getattr(pp.secondaryemail_set.first(), 'email', None),
                'sex': pp.sex,
                'language': pp.language,
                'multilingual': pp.multilingual,
                'dyslexic': pp.dyslexic,
                'created': pp.created.strftime('%Y-%m-%d')
            })
        yield io.getvalue()
