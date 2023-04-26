from django.shortcuts import get_object_or_404, render

from .models import UserProjects, Projects
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.db.models import Q

def new_project(request):
    print(request)
    # Создаём проект
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
                except:
                    pass

    

@login_required
def projects(request):
    if request.method == "POST":
        new_project(request.POST)

    # Отображение списка проектов
    projects = UserProjects.objects.filter(user=request.user)
    users_list = User.objects.all()

    return render(request, 'projects.html', {'project_list' : projects, 'user_list' : users_list,})

def projects_search_results(request):
    if request.method == "POST":
        new_project(request.POST)

    query = request.GET.get('search')

    projects_searh_list = UserProjects.objects.filter(Q(user=request.user), Q(project__project_name__icontains=query))
    users_list = User.objects.all()
    
    return render(request, 'projects_search_results.html', {'project_list' : projects_searh_list, 'user_list' : users_list})
