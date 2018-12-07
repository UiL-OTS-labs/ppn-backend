from django.views import generic
from django.views.generic.edit import ModelFormMixin, FormMixin
from django.contrib import messages
import braces.views as braces
from django.http import Http404
from django.utils.translation import ugettext as _


class HomeView(braces.LoginRequiredMixin, generic.TemplateView):
    template_name = 'main/index.html'


#
# Base classes and mixins
#

class ModelFormListView(ModelFormMixin, generic.ListView):

    def __init__(self, *args, **kwargs):
        super(ModelFormListView, self).__init__(*args, **kwargs)

        self.object = None

    def get(self, request, *args, **kwargs):
        # From ProcessFormMixin
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)

        # From BaseListView
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(
                _(u"Empty list and '%(class_name)s.allow_empty' is False.")
                % {'class_name': self.__class__.__name__}
            )

        context = self.get_context_data(object_list=self.object_list,
                                        form=self.form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class FormListView(FormMixin, generic.ListView):

    def __init__(self, *args, **kwargs):
        super(FormListView, self).__init__(*args, **kwargs)

        self.object = None

    def get(self, request, *args, **kwargs):
        # From ProcessFormMixin
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)

        # From BaseListView
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(
                _(u"Empty list and '%(class_name)s.allow_empty' is False.")
                % {'class_name': self.__class__.__name__}
            )

        context = self.get_context_data(object_list=self.object_list,
                                        form=self.form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)



class RedirectSuccessMessageMixin:
    success_message = ''

    def get(self, *args, **kwargs):
        response = super(RedirectSuccessMessageMixin, self).get(*args, **kwargs)

        messages.success(self.request, self.success_message)

        return response

    def get_success_message(self):
        return self.success_message
