from django.contrib import admin
from .models import *


@admin.register(TestCases)
class TestCasesAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        if not hasattr(instance, 'caseCreated_by'):
            instance.caseCreated_by = request.user
        obj.caseLastModified_by = request.user
        obj.save()

    list_display = ('testCase_id', 'title', 'project', 'isAutomated', 'caseCreated_by',
                    'caseCreated_date', 'caseLastModified_by', 'caseLastModified_date')
    readonly_fields = ('caseCreated_by', 'caseCreated_date',
                       'caseLastModified_by', 'caseLastModified_date')
    fieldsets = (
        (None, {
            'fields': (('title', 'status'), 'precondition', 'description', 'expectedResult')
        }),
        ('Параметры', {
            'fields': (('project', 'suite'), ('priority', 'type'), 'isAutomated', )
        }),
    )

@admin.register(TestCaseSteps)
class TestCaseStepsAdmin(admin.ModelAdmin):
    list_display = ('testCase', 'testStep', 'testCaseStep_num')
    fieldsets = (
        (None, {
            'fields': ('testCase',)
        }),
        (None, {
            'fields': (('testCaseStep_num', 'testStep'),)
        }),
    )

admin.site.register(TestSteps)
admin.site.register(Projects)
admin.site.register(UserProjects)
admin.site.register(TestPriorities)
admin.site.register(TestStatuses)
admin.site.register(TestSuites)
admin.site.register(TestTypes)

# Register your models here.
