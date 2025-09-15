from django.forms.widgets import Widget

from cdh.core.middleware import get_current_request


class LanguageWidget(Widget):
    template_name = 'widgets/language_widget.html'

    def value_from_datadict(self, data, files, name):
        value = data.get(name)

        if value == "OTHER":
            value = data.get(name + '_other')

        return value

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        context['request'] = get_current_request()

        if context['widget']['value'] not in ['nl', 'I', None]:
            context['widget']['other_value'] = context['widget']['value']
            context['widget']['value'] = 'OTHER'

        return context


class SexWidget(Widget):
    template_name = 'widgets/sex_widget.html'

    def value_from_datadict(self, data, files, name):
        value = data.get(name)

        if value == "OTHER":
            value = data.get(name + '_other')
            # Fill in 'O', if nothing was specified (which is allowed!)
            if not value:
                value = 'O'

        return value

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        context['request'] = get_current_request()

        if context['widget']['value'] not in ['M', 'F', 'PNTA', None]:
            context['widget']['other_value'] = context['widget']['value']
            context['widget']['value'] = 'OTHER'

        return context
