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
    user = models.ForeignKey(User, verbose_name=_(
        "Пользователь"), on_delete=models.PROTECT)
    
    class Meta:
        verbose_name = _("Проект пользователя")
        verbose_name_plural = _("Проекты пользователя")

    def __str__(self):
        return f'{self.user} - {self.project}'

    def get_absolute_url(self):
        return reverse("user_project_detail", kwargs={"user": self.user, "project": self.project})
    
class TestCases(models.Model):

    testCase_id = models.AutoField(_("Код тест-кейса"), primary_key=True)
    """
    Описание тест-кейса
    """
    title = models.CharField(_("Названеи"), max_length=100)
    precondition = models.TextField(_("Предусловия"))
    description = models.TextField(_("Описание"))
    expectedResult = models.TextField(_("Ожидаемый результат"))

    """
    Параметры тест кейса:
    - Проект
    - Группа
    - Тип теста
    - Приоритет
    - Статус
    - Автоматизирован (True/False)
    """
    project = models.ForeignKey(Projects, verbose_name=_("Проект"), on_delete=models.PROTECT)
    #suite = models.ForeignKey(TetSuites, verbose_name=_("Группа"), on_delete=models.PROTECT)
    #type = models.ForeignKey(TestTypes, verbose_name=_("Тип"), on_delete=models.CASCADE)
    #priority = models.ForeignKey(TestPriorities, verbose_name=_("Приоритет"), on_delete=models.CASCADE)
    #status = models.ForeignKey(TestStatuses, verbose_name=_("Статус"), on_delete=models.CASCADE)
    isAutomated = models.BooleanField(_("Автоматизирован"))

    """
    Кем и когда создано
    """    
    caseCreated_by = models.ForeignKey(User, verbose_name="Создатель", on_delete=models.PROTECT, related_name='created_by')
    caseCreated_date = models.DateTimeField(_("Создано"))

    """
    Кем и когда модифицировано
    """
    caseLastModified_by = models.ForeignKey(User, verbose_name="Последние изменения", on_delete=models.PROTECT, related_name='modified_by')
    caseLastModified_date = models.DateTimeField(_("Изменено"))
      
    class Meta:
        verbose_name = _("Тест-кейс")
        verbose_name_plural = _("Тест-кейсы")

    def __str__(self):
        return f'[{self.testCase_id}] - {self.title}'

    def get_absolute_url(self):
        return reverse("test_case_detail", kwargs={"pk": self.pk})

