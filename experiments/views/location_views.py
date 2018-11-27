from django.views import generic
from django.urls import reverse
import braces.views as braces

from ..models import Location
from ..forms import CreateLocationForm


class LocationHomeView(braces.LoginRequiredMixin, generic.ListView):
    template_name = 'locations/index.html'
    model = Location


class CreateLocationView(braces.LoginRequiredMixin, generic.CreateView):
    template_name = 'locations/new.html'
    form_class = CreateLocationForm

    def get_success_url(self):
        return reverse('experiments:location_home')


class UpdateLocationView(braces.LoginRequiredMixin, generic.UpdateView):
    template_name = 'locations/edit.html'
    form_class = CreateLocationForm
    model = Location

    def get_success_url(self):
        return reverse('experiments:location_home')