from django.utils.translation import gettext_lazy as _

from cdh.mail.classes import BaseCustomTemplateEmail, CTEVarDef

DEFAULT_SENDER = "Taal-experimenten"

DEFAULT_INVITE_FOOTER = "<p>Je ontvangt deze e-mail omdat je je e-mailadres" \
                        " hebt opgegeven om informatie te ontvangen over " \
                        "nieuwe experimenten in de ILS Labs. Indien je deze " \
                        "e-mails niet meer wilt ontvangen klik dan " \
                        "<a href=\"{{ unsub_link }}\" " \
                        "style=\"color:#fff\">hier</a>.</p>"

DEFAULT_REMINDER_FOOTER = "Dit bericht is automatisch verzonden omdat je je " \
                          "hebt ingeschreven voor een experiment."

DEFAULT_CONFIRMATION_FOOTER = "<p>Dit bericht is automatisch verzonden omdat " \
                              "je je hebt ingeschreven voor een experiment.</p>"

DEFAULT_CONFIRMATION_CONTENT = """<p>Beste {{ name }},</p>
    <p>
        Je hebt een afspraak gemaakt om mee te doen met het experiment: 
        <strong>{{ experiment_name }}</strong><br/><br/>
        We verwachten je op:<br/><br/>
        Datum: <strong>{{ date }}</strong><br/>
        Tijd: <strong>{{ time }} uur</strong><br/>
        Locatie: <strong>{{ experiment_location }}</strong><br/>
    </p>
    <p>
        Als je deze afspraak wilt afzeggen, kun je dat doen via 
        <a href="{{ cancel_link }}">deze link</a>.
        Doe dat alsjeblieft minstens 24 uur vantevoren. Als je vlak vantevoren 
        ontdekt dat je verhinderd bent, neem dan svp even persoonlijk contact 
        op met de proefleider 
        ({{ leader_name }}, email: {{ leader_email }} tel.: 
        {{ leader_phonenumber }}).
    </p>
    <p>
        Met vriendelijke groet,<br/>
        de ILS Labs
    </p>"""

DEFAULT_INVITE_CONTENT = """<p>Je kunt je weer opgeven voor een nieuw 
    experiment: <strong>{{ experiment_name }}</strong>.</p>
<p>De proefleider is <strong>{{ leader_name }}</strong>.
<ul>
    <li>Duur: {{ duration }}.</li>
    <li>Vergoeding: {{ compensation }}.</li>
    <li>{{ task_description }}</li>
    <li>{{ additional_instructions }}</li>
</ul>

<p>Je kunt via <a href="{{ reg_link }}">deze link</a> inschrijven.</p>

<p>Bedankt!</p>

<p>
Met vriendelijke groet,<br/>
{{ admin }}
</p>"""

DEFAULT_REMINDER_CONTENT = """<p>Beste {{ name }},</p>
    <p>
        <strong>Dit is een reminder!</strong>
    </p>
    <p>
        Je hebt een afspraak gemaakt om mee te doen met het experiment: 
        <strong> {{ experiment_name }}</strong>.
    </p>
    <p>
        We verwachten je op: <br/>
        Datum: <strong>{{ date }}</strong><br/>
        Tijd: <strong>{{ time }} uur</strong><br/>
        Locatie: <strong>{{ experiment_location }}</strong><br/>
    </p>
    <p>
        Als je deze afspraak wilt afzeggen, kun je dat doen via 
        <a href="{{ cancel_link }}">deze link</a>. Doe dat alsjeblieft 
        minstens 24 uur vantevoren. Als je vlak vantevoren ontdekt dat je 
        verhinderd bent, neem dan svp even persoonlijk contact op met de 
        proefleider ({{ leader_name }}, email: {{ leader_email }}
        tel.: {{ leader_phonenumber }}).
    </p>"""


class InviteEmail(BaseCustomTemplateEmail):
    user_variable_defs = [
        CTEVarDef(
            'name',
            _("invite-email.vars.name"),
            "proefpersoon",
        ),
        CTEVarDef(
            'duration',
            _("invite-email.vars.duration"),
            safe=True,
        ),
        CTEVarDef(
            'compensation',
            _("invite-email.vars.compensation"),
            safe=True,
        ),
        CTEVarDef(
            'task_description',
            _("invite-email.vars.task_description"),
            safe=True,
        ),
        CTEVarDef(
            'additional_instructions',
            _("invite-email.vars.additional_instructions"),
            safe=True,
        ),
        CTEVarDef(
            'experiment_name',
            _("invite-email.vars.experiment_name"),
            safe=True,
        ),
        CTEVarDef(
            'experiment_location',
            _("invite-email.vars.experiment_location"),
            safe=True,
        ),
        CTEVarDef(
            'leader_name',
            _("invite-email.vars.leader_name"),
            safe=True,
        ),
        CTEVarDef(
            'leader_email',
            _("invite-email.vars.leader_email"),
            safe=True,
        ),
        CTEVarDef(
            'leader_phonenumber',
            _("invite-email.vars.leader_phonenumber"),
            safe=True,
        ),
        CTEVarDef(
            'all_leaders_name_list',
            _("invite-email.vars.all_leaders_name_list"),
            safe=True,
        ),
        CTEVarDef(
            'admin',
            _("invite-email.vars.admin"),
            safe=True,
        ),
        CTEVarDef(
            'reg_link',
            _("invite-email.vars.reg_link"),
            safe=True,
        ),
    ]
    default_content = DEFAULT_INVITE_CONTENT

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sender = DEFAULT_SENDER
        self.banner = "Uitnodiging deelname experiment: <strong>{{ " \
                      "experiment_name }}</strong>"
        if self.footer is None:
            self.footer = DEFAULT_INVITE_FOOTER
        self.language = 'nl'


class ReminderEmail(BaseCustomTemplateEmail):
    user_variable_defs = [
        CTEVarDef(
            'name',
            _("reminder-email.vars.name"),
            "proefpersoon",
        ),
        CTEVarDef(
            'experiment_name',
            _("reminder-email.vars.experiment_name"),
            safe=True,
        ),
        CTEVarDef(
            'experiment_location',
            _("reminder-email.vars.experiment_location"),
            safe=True,
        ),
        CTEVarDef(
            'date',
            _("reminder-email.vars.date"),
            "Dinsdag 10-11-2011",
            safe=True,
        ),
        CTEVarDef(
            'time',
            _("reminder-email.vars.time"),
            "13:40",
            safe=True,
        ),
        CTEVarDef(
            'leader_name',
            _("reminder-email.vars.leader_name"),
            safe=True,
        ),
        CTEVarDef(
            'leader_email',
            _("reminder-email.vars.leader_email"),
            safe=True,
        ),
        CTEVarDef(
            'leader_phonenumber',
            _("reminder-email.vars.leader_phonenumber"),
            safe=True,
        ),
        CTEVarDef(
            'all_leaders_name_list',
            _("reminder-email.vars.all_leaders_name_list"),
            safe=True,
        ),
        CTEVarDef(
            'admin',
            _("reminder-email.vars.admin"),
            safe=True,
        ),
        CTEVarDef(
            'cancel_link',
            _("reminder-email.vars.cancel_link"),
            safe=True,
        ),
    ]
    default_content = DEFAULT_REMINDER_CONTENT

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sender = DEFAULT_SENDER
        self.banner = "Herinnering afspraak experiment " \
                      "<strong>{{ experiment.name }}</strong>"
        if self.footer is None:
            self.footer = DEFAULT_REMINDER_FOOTER
        self.language = 'nl'


class ConfirmationEmail(BaseCustomTemplateEmail):
    user_variable_defs = [
        CTEVarDef(
            'name',
            _("confirmation-email.vars.name"),
            "proefpersoon"
        ),
        CTEVarDef(
            'experiment_name',
            _("confirmation-email.vars.experiment_name"),
            safe=True,
        ),
        CTEVarDef(
            'experiment_location',
            _("confirmation-email.vars.experiment_location"),
            safe=True,
        ),
        CTEVarDef(
            'date',
            _("confirmation-email.vars.date"),
            "Dinsdag 10-11-2011",
            safe=True,
        ),
        CTEVarDef(
            'time',
            _("confirmation-email.vars.time"),
            "13:40",
            safe=True,
        ),
        CTEVarDef(
            'leader_name',
            _("confirmation-email.vars.leader_name"),
            safe=True,
        ),
        CTEVarDef(
            'leader_email',
            _("confirmation-email.vars.leader_email"),
            safe=True,
        ),
        CTEVarDef(
            'leader_phonenumber',
            _("confirmation-email.vars.leader_phonenumber"),
            safe=True,
        ),
        CTEVarDef(
            'all_leaders_name_list',
            _("confirmation-email.vars.all_leaders_name_list"),
            safe=True,
        ),
        CTEVarDef(
            'cancel_link',
            _("confirmation-email.vars.cancel_link"),
            safe=True,
        ),
    ]
    default_content = DEFAULT_CONFIRMATION_CONTENT

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sender = DEFAULT_SENDER
        self.banner = "Bevestiging inschrijving experiment: <strong>{{ " \
                      "experiment_name }}</strong>"
        if self.footer is None:
            self.footer = DEFAULT_CONFIRMATION_FOOTER
        self.language = 'nl'
