from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import TestCasePlans, TestCaseResults, TestCaseTags, TestPlans, UserProjects, Projects, TestCases, TestSuites, TestCaseSteps
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.template.defaulttags import register
from django.db.models import Q


@register.filter
def get_item(dictionary, key):
    return dictionary[key]

# Метод для создания проетка


def create_project(request):

    project_name = request.get('project_name')

    if project_name:
        # Cоздаём проект
        project = Projects(name=project_name)
        project.save()

        # Добавляем пользователей к созданному проекту
        users_list = request.getlist('project_users')
        if users_list:
            for user in users_list:
                try:
                    uid = User.objects.get(username=user)
                    user_project = UserProjects(project=project, user=uid)
                    user_project.save()
                except Exception:
                    raise

# Список проектов


@login_required
def projects(request):
    if request.method == "POST":
        create_project(request.POST)
        return redirect(request.META['HTTP_REFERER'])

    # Отображение списка проектов
    projects = UserProjects.objects.filter(user=request.user)
    users_list = User.objects.all()

    return render(request, 'projects/projects.html', {'project_list': projects, 'user_list': users_list, })

# Удаление выбранных тестов


def tests_remove(request):
    test_ids = request.POST.getlist('test_ids[]')
    for id in test_ids:
        test = TestCases.objects.get(id=id)
        test.delete()

    return HttpResponseRedirect(reverse('tests'))

# Список тестов


def tests(request):

    suite_list = TestSuites.objects.all()

    suite_test_list = dict()
    testCaseSteps = dict()
    testCase_tags = dict()

    for suite_iter in suite_list:
        tests = TestCases.objects.filter(
            suite=suite_iter).order_by('title')

        suite_test_list[suite_iter.name] = tests

        for test in tests:
            testCaseSteps[test.id] = TestCaseSteps.objects.filter(
                testCase=test)
            testCase_tags[test.id] = TestCaseTags.objects.filter(
                testCase=test.id
            )
    print(testCaseSteps)
    return render(request, 'tests.html', {
        'suite_list': suite_list,
        'suite_test_list': suite_test_list,
        'testCaseSteps': testCaseSteps,
        'testCaseTags': testCase_tags,
    })

# Список тест-планов


def test_plans(request, project_pk):
    if request.method == "POST":
        create_testPlan(request.POST)
        return redirect(request.META['HTTP_REFERER'])

    project = Projects.objects.get(id=project_pk)
    testPlans_list = TestPlans.objects.filter(project__id=project_pk)
    project_testCases = TestCases.objects.filter(project__id=project_pk)
    project_users = UserProjects.objects.filter(project=project_pk)

    testPlans_testCase_dict = dict()
    testCase_steps = dict()
    testCase_tags = dict()

    # What the fuck
    '''
    Попробую объяснить
    1. Получаем список айдишников тест-планов проекта
    2. Для каждого айдишника получаем QuerySet объектов TestCasePlans
    3. Для каждого значения QuerySet - TestCasePlans получаем TestCase
    4. Заносим все TestCase для айдишника плана в список и добавляем его в словарь

    Итог:
    Словарь вида:
    testPlan_id |   1   |    2   |   3   |
                |-------|--------|-------|
                |  TC1  |   TC6  |       |
                |  TC2  |   TC7  |       |
                |  TC3  |        |       |
                |       |        |       |
    '''

    for testPlan_id in testPlans_list:
        testPlan_list = TestCasePlans.objects.filter(testPlan=testPlan_id)
        l = list()

        for testPlan in testPlan_list:
            l.append(testPlan)
            testCase_steps[testPlan.testCase.id] = TestCaseSteps.objects.filter(
                testCase__project=project, testCase=testPlan.testCase)
            testCase_tags[testPlan.testCase.id] = TestCaseTags.objects.filter(
                testCase=testPlan.testCase
            )
        testPlans_testCase_dict[testPlan_id] = l
        
    print(testCase_steps)
    return render(request, 'test_plans.html', {
        # TODO: Переименовать все
        'project': project,
        'suite_list': testPlans_list,
        'suite_test_list': testPlans_testCase_dict,
        'testCaseSteps': testCase_steps,
        'testCaseTags': testCase_tags,
        'projectTestCases': project_testCases,
        'project_users': project_users,
    }
    )

# TODO: Создание тест-плана


def create_testPlan(request):
    print('name', request.getlist('testPlan_name'))
    print('description', request.getlist('testPlan_description'))
    print('selected_row', request.getlist('selected_row'))
    print('testCase_time', request.getlist('testCase_time'))
    print('testCase_assigned', request.getlist('testCase_assigned'))
    return

# Смена результата на "Успех"


def testResult_success(request, project_pk, testPlan_pk, test_pk):
    testPlan = TestCasePlans.objects.get(
        testPlan__id=testPlan_pk, testPlan__project=project_pk, testCase__id=test_pk)
    testPlan.result = TestCaseResults.objects.get(name="Успех")
    testPlan.save()

    return redirect(request.META['HTTP_REFERER'])

# Смена результата на "Ошибка"


def testResult_fail(request, project_pk, testPlan_pk, test_pk):
    testPlan = TestCasePlans.objects.get(
        testPlan__id=testPlan_pk, testPlan__project=project_pk, testCase__id=test_pk)
    testPlan.result = TestCaseResults.objects.get(name="Ошибка")
    testPlan.save()

    return redirect(request.META['HTTP_REFERER'])

# Поиск проектов


@login_required
def projects_search_results(request):
    if request.method == "POST":
        print(request.POST)
        create_project(request.POST)

    if request.method == 'GET':
        query = request.GET.get('search')
        print(query)
        projects_searh_list = UserProjects.objects.filter(
            Q(user=request.user), Q(project__name__icontains=query))

    users_list = User.objects.all()

    return render(request, 'projects/projects_search_results.html', {'project_list': projects_searh_list, 'user_list': users_list})

# Просмотр наборов и тестов проекта


def project_view(request, project_pk):
    project = Projects.objects.get(id=project_pk)

    if request.method == "POST":
        create_suite(request.POST, project)
        return redirect(request.META['HTTP_REFERER'])

    suite_list = TestSuites.objects.filter(project=project_pk)

    suite_test_list = dict()
    testCaseSteps = dict()

    for suite_iter in suite_list:
        tests = TestCases.objects.filter(
            suite=suite_iter, project=project_pk).order_by('title')

        suite_test_list[suite_iter.name] = tests

        for test in tests:
            testCaseSteps[test.id] = TestCaseSteps.objects.filter(
                testCase__project=project, testCase=test)

    return render(request, 'projects/project_view.html', {
        'project': project,
        'suite_list': suite_list,
        'suite_test_list': suite_test_list,
        'testCaseSteps': testCaseSteps
    }
    )

# Создание набора


def create_suite(request, project_req):
    suite = TestSuites(name=request.get(
        'suite_name'), project=project_req)
    suite.save()

# Удалить набор


def delete_suite(request, project_pk, suite_name):
    suite = TestSuites.objects.filter(project__id=project_pk, name=suite_name)
    suite.delete()
    return HttpResponseRedirect(reverse('project_view', args=[project_pk]))
