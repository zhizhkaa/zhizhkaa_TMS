from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import UserProjects, Projects, TestCases, TestSuites, TestCaseSteps
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.template.defaulttags import register
from django.db.models import Q


@register.filter
def get_item(dictionary, key):
    return dictionary[key]


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


@login_required
def projects(request):
    if request.method == "POST":
        create_project(request.POST)
        return redirect(request.META['HTTP_REFERER'])

    # Отображение списка проектов
    projects = UserProjects.objects.filter(user=request.user)
    users_list = User.objects.all()

    return render(request, 'projects/projects.html', {'project_list': projects, 'user_list': users_list, })


def tests(request):

    suite_list = TestSuites.objects.all()

    suite_test_list = dict()
    testCaseSteps = dict()

    for suite_iter in suite_list:
        tests = TestCases.objects.filter(
            suite=suite_iter).order_by('title')

        suite_test_list[suite_iter.name] = tests

        for test in tests:
            testCaseSteps[test.id] = TestCaseSteps.objects.filter(testCase=test)

    return render(request, 'tests.html', {
        'suite_list': suite_list,
        'suite_test_list': suite_test_list,
        'testCaseSteps': testCaseSteps
    })


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


def create_suite(request, project_req):
    suite = TestSuites(name=request.get(
        'suite_name'), project=project_req)
    suite.save()


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


def delete_suite(request, project_pk, suite_name):
    suite = TestSuites.objects.filter(project__id=project_pk, name=suite_name)
    suite.delete()
    return HttpResponseRedirect(reverse('project_view', args=[project_pk]))
