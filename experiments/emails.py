from django.utils.translation import gettext_lazy as _

from cdh.core.mail import BaseCustomTemplateEmail, CTEVarDef


class InviteEmail(BaseCustomTemplateEmail):
    user_variable_defs = [
        CTEVarDef('name', _("invite-email.vars.name"), "proefpersoon"),
        CTEVarDef('duration', _("invite-email.vars.duration")),
        CTEVarDef('compensation', _("invite-email.vars.compensation")),
        CTEVarDef('task_description', _("invite-email.vars.task_description")),
        CTEVarDef('additional_instructions', _("invite-email.vars.additional_instructions")),
        CTEVarDef('experiment_name', _("invite-email.vars.experiment_name")),
        CTEVarDef('experiment_location', _("invite-email.vars.experiment_location")),
        CTEVarDef('leader_name', _("invite-email.vars.leader_name")),
        CTEVarDef('leader_email', _("invite-email.vars.leader_email")),
        CTEVarDef('leader_phonenumber', _("invite-email.vars.leader_phonenumber")),
        CTEVarDef('all_leaders_name_list', _("invite-email.vars.all_leaders_name_list")),
        CTEVarDef('admin', _("invite-email.vars.admin")),
        CTEVarDef('reg_link', _("invite-email.vars.reg_link")),
    ]

    def __init__(self, *args, **kwargs):
        from experiments.utils.invite import DEFAULT_FOOTER

        super().__init__(*args, **kwargs)
        self.sender = "Taal-experimenten"
        self.banner = "Uitnodiging deelname experiment: <strong>{{ " \
                      "experiment_name }}</strong>"
        if self.footer is None:
            self.footer = DEFAULT_FOOTER
        self.language = 'nl'


