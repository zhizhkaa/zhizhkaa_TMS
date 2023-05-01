from django.contrib import admin
from .models import *
from django.apps import apps


models = apps.get_models()

#admin.register(TestCases)
class TestCasesAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        if not hasattr(instance, 'created_by'):
            instance.created_by = request.user
        obj.lastModified_by = request.user
        obj.save()

    list_display = ('id', 'title', 'project', 'isAutomated', 'created_by',
                    'created_date', 'lastModified_by', 'lastModified_date')
    readonly_fields = ('created_by', 'created_date',
                       'lastModified_by', 'lastModified_date')
    fieldsets = (
        (None, {
            'fields': (('title', 'status'), 'precondition', 'description', 'expectedResult')
        }),
        ('Параметры', {
            'fields': (('project', 'suite'), ('priority', 'type'), 'isAutomated', )
        }),
    )

#@admin.register(TestCaseSteps)
class TestCaseStepsAdmin(admin.ModelAdmin):
    list_display = ('testCase', 'testStep', 'index_num')
    fieldsets = (
        (None, {
            'fields': ('testCase',)
        }),
        (None, {
            'fields': (('index_num', 'testStep'),)
        }),
    )

class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super(ListAdminMixin, self).__init__(model, admin_site)

models = apps.get_models()
for model in models:
    admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass
# Register your models here.
