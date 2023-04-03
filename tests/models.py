from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Projects(models.Model):
    """
    Хранит список проектов
    """
    project_id = models.AutoField(
        primary_key=True, verbose_name=_("Код проекта"))
    
    project_name = models.CharField(max_length=50, verbose_name=_(
        "Название проекта"), help_text="Название проекта")

    class Meta:
        verbose_name = _("Проект")
        verbose_name_plural = _("Проекты")
        ordering = ['project_name']

    def __str__(self):
        return self.project_name

    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"pk": self.pk})

class UserProjects(models.Model):
    """
    Хранит связь пользователей с проектами
    """
    userProject_id = models.AutoField(
        primary_key=True, verbose_name="Код проект-пользователь")
    
    project = models.ForeignKey(
        Projects, on_delete=models.PROTECT, verbose_name="Проект")
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "Пользователь"), on_delete=models.PROTECT)

    class Meta:
        verbose_name = _("Проект пользователя")
        verbose_name_plural = _("Проекты пользователя")

    def __str__(self):
        return f'{self.project} - {self.user}'

    def get_absolute_url(self):
        return reverse("user_project_detail", kwargs={"user": self.user, "project": self.project})

class TestSuites(models.Model):

    testSuite_id = models.AutoField(_("Код набора"), primary_key=True)
    testSuite_name = models.CharField(_("Название набора"), max_length=50)

    class Meta:
        verbose_name = _("Тестовй набор")
        verbose_name_plural = _("Тестовые наборы")

    def __str__(self):
        return self.testSuite_name

    def get_absolute_url(self):
        return reverse("test_suite_detail", kwargs={"pk": self.pk})
    
class TestTypes(models.Model):

    testType_id = models.AutoField(_("Код типа"), primary_key=True)
    testType_name = models.CharField(_("Тип"), max_length=50)

    class Meta:
        verbose_name = _("Тип теста")
        verbose_name_plural = _("Типы тестов")

    def __str__(self):
        return self.testType_name

    def get_absolute_url(self):
        return reverse("test_type_detail", kwargs={"pk": self.pk})

class TestPriorities(models.Model):

    testPriority_id = models.AutoField(_("Код приоритета"), primary_key=True)
    testPriority_name = models.CharField(_("Приоритет"), max_length=50)

    class Meta:
        verbose_name = _("Приоритет")
        verbose_name_plural = _("Приоритеты")

    def __str__(self):
        return self.testPriority_name

    def get_absolute_url(self):
        return reverse("test_priority_detail", kwargs={"pk": self.pk})

class TestStatuses(models.Model):

    testStatus_id = models.AutoField(_("Код статуса"), primary_key=True)
    testStatus_name = models.CharField(_("Статус"), max_length=50)

    class Meta:
        verbose_name = _("Статус теста")
        verbose_name_plural = _("Статусы тестов")

    def __str__(self):
        return self.testStatus_name

    def get_absolute_url(self):
        return reverse("test_status_detail", kwargs={"pk": self.pk})

class TestCases(models.Model):

    testCase_id = models.AutoField(_("Код тест-кейса"), primary_key=True)
    """
    Описание тест-кейса
    """
    title = models.CharField(_("Название"), max_length=100)
    precondition = models.TextField(_("Предусловия"), blank=True, null=True)
    description = models.TextField(_("Описание"), blank=True, null=True)
    expectedResult = models.TextField(_("Ожидаемый результат"), blank=True, null=True)

    """
    Параметры тест кейса:
    - Проект
    - Набор
    - Тип теста
    - Приоритет
    - Статус
    - Автоматизирован (True/False)
    """
    project = models.ForeignKey(Projects, verbose_name=_(
        "Проект"), on_delete=models.PROTECT)
    
    suite = models.ForeignKey(TestSuites, verbose_name=_("Группа"), on_delete=models.PROTECT)
    type = models.ForeignKey(TestTypes, verbose_name=_("Тип теста"), on_delete=models.PROTECT)
    priority = models.ForeignKey(TestPriorities, verbose_name=_("Приоритет"), on_delete=models.PROTECT)
    status = models.ForeignKey(TestStatuses, verbose_name=_("Статус"), on_delete=models.PROTECT, default=3)
    isAutomated = models.BooleanField(_("Автоматизирован"))

    """
    Кем и когда создано
    """
    caseCreated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Создатель", on_delete=models.PROTECT, related_name='created_by')
    
    caseCreated_date = models.DateTimeField(_("Создано"), auto_now_add=True)

    """
    Кем и когда модифицировано
    """
    caseLastModified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Последние изменения", on_delete=models.PROTECT, related_name='modified_by')
    
    caseLastModified_date = models.DateTimeField(_("Изменено"), auto_now=True)

    class Meta:
        verbose_name = _("Тест-кейс")
        verbose_name_plural = _("Тест-кейсы")

    def __str__(self):
        return f'[{self.testCase_id}] {self.title}'

    def get_absolute_url(self):
        return reverse("test_case_detail", kwargs={"pk": self.pk})
    
class TestSteps(models.Model):

    testStep_id = models.AutoField(_("Код шага"), primary_key=True)
    project = models.ForeignKey(Projects, verbose_name=_("Проект"), on_delete=models.PROTECT)
    description = models.CharField(_("Описание шага"), max_length=100)
    expectedResult = models.TextField(_("Ожидаемый результат"))

    class Meta:
        verbose_name = _("Шаги теста")
        verbose_name_plural = _("Шаги тестов")

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse("test_step_detail", kwargs={"pk": self.pk})

class TestCaseSteps(models.Model):

    testCase = models.ForeignKey(TestCases, verbose_name=_("Тест-кейс"), on_delete=models.PROTECT)
    testStep = models.ForeignKey(TestSteps, verbose_name=_("Шаг"), on_delete=models.CASCADE)
    testCaseStep_num = models.PositiveIntegerField(_("Номер шага"))

    class Meta:
        verbose_name = _("Шаги тест-кейса")
        verbose_name_plural = _("Шаги тест-кейсов")

    def __str__(self):
        return f'{self.testCase}: {self.testCaseStep_num} - {self.testStep}'

    def get_absolute_url(self):
        return reverse("TestCaseSteps_detail", kwargs={"pk": self.pk})
