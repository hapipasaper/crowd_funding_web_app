from django.urls import path
from . import views

app_name = "projects"

urlpatterns = [
    path("create/", views.create_project, name="create_project"),   # http://127.0.0.1:8000/projects/create/
    path("<int:pk>/", views.project_detail, name="project_detail"), # http://127.0.0.1:8000/projects/1/
      path("<int:pk>/cancel/", views.cancel_project, name="cancel_project"),
      path("reports/", views.reports, name="reports"), 
       path("search/", views.project_search, name="search"),
]
