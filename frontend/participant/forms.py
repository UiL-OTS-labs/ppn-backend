from django import forms
from django.utils.safestring import mark_safe
from django.urls import reverse

from cdh.core.forms import BootstrapRadioSelect, TemplatedForm, TelephoneInput
from .widgets import LanguageWidget, SexWidget


#
# Sign up form
#

class SignUpForm(TemplatedForm):

    ACCOUNT_CHOICES = (
        (
            True,
            "Ja, ik wil een account aanmaken"
        ),
        (
            False,
            "Nee, ik wil geen account aanmaken"
        ),
    )

    MULTILINGUAL_CHOICES = (
        (
            False,
            'Eentalig'
        ),
        (
            True,
            'Meertalig (opgegroeid met meerdere moedertalen)'
        ),
    )

    MAILING_LIST_CHOICES = (
        (
            True,
            "Ja, ik wil graag bericht krijgen over nieuwe experimenten"
        ),
        (
            False,
            "Nee, ik wil geen bericht krijgen over nieuwe experimenten"
        ),
    )

    name = forms.Field(
        label="Voor- en achternaam",
        required=False,
    )

    email = forms.EmailField(
        label="Emailadres",
    )

    language = forms.CharField(
        label="Mijn moedertaal is",
        widget=LanguageWidget,
    )

    #
    # The following BooleanFields have a strange 'required' config by design.
    # To allow 'False' as a valid option, we need to specify
    # 'required=False'. However, this allows the field to accept no  answer
    # (None) as a valid value, in which case the field will return 'False'.
    # As this obviously is not what we want, we specify 'required' in the
    # widget 'attrs', so the HTML will still say the field is required,
    # prompting the user to pick the right answer for them.
    # Why this is the default behaviour of BooleanField is above me...
    #

    account = forms.BooleanField(
        label='Ik ben',
        widget=BootstrapRadioSelect(
            choices=ACCOUNT_CHOICES,
            attrs={
                'required': True,
            }
        ),
        required=False,
    )

    multilingual = forms.BooleanField(
        label='Ik ben',
        widget=BootstrapRadioSelect(
            choices=MULTILINGUAL_CHOICES,
            attrs={
                'required': True,
            }
        ),
        required=False,
    )

    dyslexic = forms.BooleanField(
        label='Ik ben',
        widget=BootstrapRadioSelect(
            choices=(
                (True, 'Dyslectisch'),
                (False, 'Niet dyslectisch'),
            ),
            attrs={
                'required': True,
            }
        ),
        required=False,
    )

    mailing_list = forms.BooleanField(
        label='Ik wil',
        widget=BootstrapRadioSelect(
            choices=MAILING_LIST_CHOICES,
            attrs={
                'required': True,
            }
        ),
        required=False,
    )

    consent = forms.BooleanField(
        label='Dataverwerking',
        widget=BootstrapRadioSelect(
            choices=(
                (
                    True,
                    ('Ja, ik geef uitdrukkelijke toestemming om mijn gegevens '
                     '(inclusief antwoorden op eventuele gevoelige vragen) op '
                     'te slaan t.b.v. van het verwerken van mijn aanmelding, '
                     'en om deze gegevens te delen met de proefleider.')
                ),
            ),
            attrs={
                'required': 'required'
            }
        ),
        required=True
    )

    def clean(self):
        """
        Two tasks:

        Make sure the user has entered a name if creating an account.
        The field is not marked as required, as the requirement is conditional.

        Make sure the user has selected at least one of account/mailinglist
        """
        account = self.cleaned_data.get('account', False)
        name = self.cleaned_data.get('name', None)

        if account and not name:
            self.add_error('name', "Dit veld is verplicht")

        mailing_list = self.cleaned_data.get('mailing_list', False)

        if not account and not mailing_list:
            # It's an error on both, but we'll just add it to account as twice
            # is redundant
            self.add_error('account', "Kies a.u.b. om je in te schrijven voor "
                                      "de mailinglist en/of om een account aan "
                                      "te maken.")

        return self.cleaned_data

    def clean_email(self):
        data = self.cleaned_data.get('email')

        # Local import, as participants.utils imports this module. (We don't
        # want cycles!)
        from participant.utils import check_if_email_is_spammer
        if check_if_email_is_spammer(data):
            self.add_error(
                'email',
                'Dit emailadres staat bekend als een adres waarvandaan spam '
                'wordt verzonden, vul ajb een ander adres in.'
            )

        return data

    def get_context(self):
        context = super().get_context()
        # Remove the fields we add manually from the context
        context['fields'] = [
            x for x in context['fields']
            if x[0].name not in ['account', 'mailing_list', 'consent']
        ]
        return context

#
# Register form
#

class BaseRegisterForm(TemplatedForm):
    show_help_column = False
    always_show_help_column = False

    name = forms.CharField(
        label="Naam",
        help_text=mark_safe(
            "Zie ook onze <a href='/privacy/'>privacy-verklaring</a> voor meer "
            "informatie over waarom we deze gegevens nodig hebben en hoe wij "
            "hier mee om gaan."
        )
    )

    email = forms.EmailField(
        label="Emailadres",
    )

    phone = forms.CharField(
        label="Telefoonnummer",
        widget=TelephoneInput,
        help_text=mark_safe(
            "<strong>Waarom willen we je telefoonummer weten?</strong><br> "
            "We vragen dit zodat we je kunnen bellen als bijvoorbeeld je "
            "afspraak op het laatste moment niet door kan gaan of je de "
            "weg niet kunt vinden in het lab."
        )
    )

    birth_date = forms.DateField(
        label="Geboortedatum",
        widget=forms.DateInput(attrs={
            'placeholder': 'dd-mm-yyyy',
            'pattern': '[0-9-]+',
        }),
    )

    language = forms.CharField(
        label="Mijn moedertaal is",
        widget=LanguageWidget,
    )

    multilingual = forms.CharField(
        label='Ik ben',
        widget=BootstrapRadioSelect(
            choices=(
                ('N', 'Eentalig'),
                ('Y', 'Meertalig (opgegroeid met meerdere moedertalen)'),
            ),
        ),
    )

    sex = forms.CharField(
        label=lambda: mark_safe(f'Mijn <a href="'
                                f'{reverse("main:privacy")}#biological-sex"'
                                f'target="_blank">'
                                f'biologisch geslacht</a> is'),
        help_text=mark_safe(
            '<strong>Waarom willen we je biologisch geslacht weten?</strong>'
            '<br>'
            'Geslachtshormonen zijn van invloed op de ontwikkeling en '
            'het functioneren van de hersenen, en kunnen dus ook '
            'invloed hebben op hoe de hersenen met taal omgaan. Het is '
            'daarom gebruikelijk om op groepsniveau te rapporteren '
            'hoeveel mannen en hoeveel vrouwen aan een studie hebben '
            'deelgenomen. Soms worden de resultaten ook per groep '
            'geanalyseerd.'
        ),
        widget=SexWidget
    )

    handedness = forms.CharField(
        label='Ik ben',
        help_text=mark_safe(
            '<strong>Waarom willen we weten wat je dominante hand is?</strong>'
            '<br>Links- danwel rechtshandigheid gaat gepaard met verschillen in'
            ' de hersenen, die ook van invloed zouden kunnen zijn op hoe de '
            'hersenen met taal omgaan. Het is daarom gebruikelijk om op '
            'groepsniveau te rapporteren hoeveel links- en rechtshandigen aan '
            'een studie hebben deelgenomen. Soms worden de resultaten ook per '
            'groep geanalyseerd.'
        ),
        widget=BootstrapRadioSelect(
            choices=(
                ('L', 'Linkshandig'),
                ('R', 'Rechtshandig'),
            ),
        ),
    )

    dyslexic = forms.CharField(
        label='Ik ben',
        widget=BootstrapRadioSelect(
            choices=(
                ('Y', 'Dyslectisch'),
                ('N', 'Niet dyslectisch'),
            ),
        )
    )

    social_status = forms.CharField(
        label='Ik ben',
        widget=BootstrapRadioSelect(
            choices=(
                ('S', 'Student'),
                ('O', 'Geen student'),
            ),
        )
    )

    def clean_email(self):
        data = self.cleaned_data.get('email')

        # Local import, as participants.utils imports this module. (We don't
        # want cycles!)
        from participant.utils import check_if_email_is_spammer
        if check_if_email_is_spammer(data):
            self.add_error(
                'email',
                'Dit emailadres staat bekend als een adres waarvandaan spam '
                'wordt verzonden, vul ajb een ander adres in.'
            )

        return data
