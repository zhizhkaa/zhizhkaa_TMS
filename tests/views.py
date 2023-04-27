from django.shortcuts import render

from .models import UserProjects, Projects, TestCases, TestSuites
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.db.models import Q


def create_project(request):

    project_name = request.get('project_name')

    if project_name:
        project = Projects(project_name=project_name)
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

    # Отображение списка проектов
    projects = UserProjects.objects.filter(user=request.user)
    users_list = User.objects.all()

    return render(request, 'projects.html', {'project_list': projects, 'user_list': users_list, })


@login_required
def projects_search_results(request):
    if request.method == "POST":
        create_project(request.POST)

    query = request.GET.get('search')

    projects_searh_list = UserProjects.objects.filter(
        Q(user=request.user), Q(project__project_name__icontains=query))
    users_list = User.objects.all()

    return render(request, 'projects_search_results.html', {'project_list': projects_searh_list, 'user_list': users_list})


def create_suite(request, project):
    suite = TestSuites(testSuite_name=request.get('suite_name'), project=project)
    suite.save()

def project_view(request, project_pk):    
    project = Projects.objects.get(project_id=project_pk)

    if request.method == "POST":
        create_suite(request.POST, project)

    suite_list = TestSuites.objects.filter(project=project_pk)

    suite_test_list = list()

    for suite_iter in suite_list:
        suite_test_list.append(list(TestCases.objects.filter(suite=suite_iter, project=project_pk).order_by('title')))

    print(suite_test_list)
    print(request.POST)

    return render(request, 'project_view.html', {'project': project, 'suite_list': suite_list, 'suite_test_list': suite_test_list})
