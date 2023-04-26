from django.urls import path


from . import views

urlpatterns = [
    path('projects/', views.projects, name='projects'),
    path('search', views.projects_search_results, name='search_results'),
]