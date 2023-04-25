from django.shortcuts import render
from .models import UserProjects
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

@login_required
def projects(request):
    projects = UserProjects.objects.filter(user=request.user)
    users_list = User.objects.all()
    return render(request, 'projects.html', {'projects' : projects, 'users' : users_list})
