from django.urls import path


from . import views

urlpatterns = [
    path('projects/', views.projects, name='projects'),
    path('search', views.projects_search_results, name='search_results'),
    path('project/<int:project_pk>/', views.project_view, name='project_view'),
    path('project/<int:project_pk>/<int:testCase_pk>/', views.testCase_view, name='testCase_view'),
]