from django.conf.urls import url, include
from .views import (ExperimentHomeView, ExperimentCreateView,
                    ExperimentUpdateView, ExperimentEditExcludedExperimentsView,
                    ExperimentExcludeOtherExperimentView,
                    ExperimentSwitchOpenView, ExperimentSwitchVisibleView,
                    ExperimentSwitchPublicView,
                    LocationHomeView, LocationCreateView, UpdateLocationView,
                    CriteriaHomeView, DefaultCriteriaUpdateView,)

app_name = 'experiments'

urlpatterns = [
    url(r'^$', ExperimentHomeView.as_view(), name='home'),
    url(r'^new/$', ExperimentCreateView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', ExperimentUpdateView.as_view(), name='update'),

    url(
        r'^(?P<experiment>\d+)/excluded_experiments/$',
        ExperimentEditExcludedExperimentsView.as_view(),
        name='excluded_experiments'
    ),
    url(
        r'^(?P<current_experiment>\d+)/exclude_experiment/('
        r'?P<exclude_experiment>\d+)/$',
        ExperimentExcludeOtherExperimentView.as_view(),
        name='exclude_experiment'
    ),

    url(
        r'^(?P<experiment>\d+)/default_criteria/$',
        DefaultCriteriaUpdateView.as_view(),
        name='default_criteria'
    ),


    url(r'(?P<pk>\d+)/switch_open/', ExperimentSwitchOpenView.as_view(),
        name='switch_open'),
    url(r'(?P<pk>\d+)/switch_visible/', ExperimentSwitchVisibleView.as_view(),
        name='switch_visible'),
    url(r'(?P<pk>\d+)/switch_public/', ExperimentSwitchPublicView.as_view(),
        name='switch_public'),

    url(r'^locations/', include([
        url(r'^$', LocationHomeView.as_view(), name='location_home'),
        url(r'^new/$', LocationCreateView.as_view(), name='location_create'),
        url(r'^(?P<pk>\d+)/$', UpdateLocationView.as_view(),
            name='location_update')
    ])),

    url(r'^criteria/', include([
        url(r'^$', CriteriaHomeView.as_view(), name='criteria_home'),

    ])),
]
