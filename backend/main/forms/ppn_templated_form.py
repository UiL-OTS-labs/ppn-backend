from cdh.core.forms import TemplatedForm, TemplatedModelForm

class PPNTemplatedForm(TemplatedForm):
    show_valid_fields = False


class PPNTemplatedModelForm(TemplatedModelForm):
    show_valid_fields = False
