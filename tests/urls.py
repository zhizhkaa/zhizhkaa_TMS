from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views

urlpatterns = [
    path('projects/', views.projects, name='projects'),
    path('search', views.projects_search_results, name='search_results'),
    path('project/<int:project_pk>/', views.project_view, name='project_view'),
    path('project/<int:project_pk>/test_plans/', views.test_plans, name='test_plans'),
    path('project/<int:project_pk>/test_plans/<int:testPlan_pk>/<int:test_pk>/success', views.testResult_success, name='testResult_success'),
    path('project/<int:project_pk>/test_plans/<int:testPlan_pk>/<int:test_pk>/fail', views.testResult_fail, name='testResult_fail'),
    path('project/<int:project_pk>/delete/suite/<suite_name>', views.delete_suite, name='delete_suite'),
    path('tests/', views.tests, name='tests'),
    path('tests/remove/', views.tests_remove, name='tests_remove')
]