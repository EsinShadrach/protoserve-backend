from django.urls import path

from core import views

urlpatterns = [
    path("", views.endpoints, name="endpoint"),
    path("users/", views.users, name="users"),
    path("users/<str:first_name>", views.userDetailed, name="user-details"),
    
    path("experiences/", views.experiences, name="experiences"),
    path("experiences/<str:name>/", views.experiencesDetails, name="experiences-detailed"),
    
    path("educations/", views.education, name="education"),
    path("educations/<str:school_name>/", views.educationDetails, name="education-detailed"),
    
    path("projects/", views.project, name="project"),
    path("projects/<str:project_name>/", views.projectDetailed, name="project-detailed"),
    
    path("people/", views.people, name="people"),
    path("person/<int:id>", views.person, name="person"),
    
]