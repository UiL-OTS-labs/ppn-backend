from cdh.vue.components import Vue, VueComponent

Vue.add_component(VueComponent(
    'ExperimentList',
    'main/ExperimentList.vue',
    depends=['FancyList'],
    subcomponents=[],
))
