from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core import serializers
from core.models import CustomUser, Education, Experiences, Person, Project
from django.db.models import Q
from core.serializers import EducationSerializer, ExperienceSerializer, PersonSerializer, ProjectSerializer, UserSerializer
# Create your views here.

# ! YOU SHOULD ONLY BE ABLE TO SEE YOUR OWN DATA SO RESTRICTED VIEWS
@api_view(['GET'])
def endpoints(request) -> Response:
    link = 'http://127.0.0.1:8000'
    endpoint_list: list[str] = [
        f'{link}/educations/',
        '/education/:school_name',
        
        f'{link}/experience',
        '/experiences/:name',
        
        f'{link}/projects',
        '/projects/:project_name',
        
        # ! PEOPLE WOULD BE HIDDEN BUT NOT `PERSON`
        f'{link}/people',
        'person/:id',
           
        # ! USER WOULD BE HIDDEN
        f'{link}/user',
        '/user/:first_name'
    ]
    return Response(endpoint_list)


@api_view(['GET', 'POST'])
def users(request) -> Response | None:
    if request.method == "GET":
        query = request.GET.get('query')
        if query == None:
            query: str = ''
            
        users = CustomUser.objects.filter(
            Q(name__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
        serializer = UserSerializer(users, many=True)
        return Response(
            serializer.data
        )


@api_view(['GET', 'PUT', "DELETE"])
def userDetailed(request, first_name) -> Response | None:
    users = CustomUser.objects.get(first_name=first_name)

    if request.method == "GET":
        serializer = UserSerializer(users, many=False)
        return Response(serializer.data)


@api_view(["GET"])
def experiences(request) -> Response | None:
    if request.method == "GET":
        query: str | None = request.GET.get("query")
        if query == None:
            query: str = ''

        experiences = Experiences.objects.filter(
            Q(name__icontains=query) |
            Q(role__icontains=query) |
            Q(start_year__icontains=query) |
            Q(skill__icontains=query)
        )
        serializer = ExperienceSerializer(experiences, many=True)
        return Response(serializer.data)


@api_view(["GET", "PUT", "DELETE"])  # ! ADDING ABILITY TO GET PUT AND DELETE
def experiencesDetails(request, name) -> Response | None:
    experiences: Experiences = Experiences.objects.get(name=name)
    if request.method == "GET":
        serializer = ExperienceSerializer(experiences, many=False)
        return Response(serializer.data)
    # TODO: IMPLEMENT PUT AND DELETE HERE


@api_view(["GET"])
def education(request) -> Response | None:
    if request.method == "GET":
        query: str | None = request.GET.get("query")
        if query == None:
            query: str = ''

        education = Education.objects.filter(
            Q(school_name__icontains=query) |
            Q(start_year__icontains=query) |
            Q(degree__icontains=query)
        )
        serializer = EducationSerializer(education, many=True)
        return Response(serializer.data)


@api_view(["GET", "PUT", "DELETE"])  # ! ADDING ABILITY TO GET PUT AND DELETE
def educationDetails(request, school_name) -> Response | None:
    education: Education = Education.objects.get(school_name=school_name)
    if request.method == "GET":
        serializer = EducationSerializer(education, many=False)
        return Response(serializer.data)


@api_view(["GET"])
def project(request) -> Response | None:
    if request.method == "GET":
        query: str | None = request.GET.get("query")
        if query == None:
            query: str = ''

        project = Project.objects.filter(
            Q(project_name__icontains=query) |
            Q(tools__icontains=query) |
            Q(about_project__icontains=query) |
            Q(year__icontains=query) |
            Q(category__icontains=query)
        )
        serializer = ProjectSerializer(project, many=True)
        return Response(serializer.data)


@api_view(["GET", "PUT", "DELETE"])
def projectDetailed(request, project_name) -> Response | None:
    project: Project = Project.objects.get(project_name=project_name)
    if request.method == "GET":
        serializer = ProjectSerializer(project, many=False)
        return Response(serializer.data)

@api_view(["GET"])
def person(request, id) -> Response:
    person: Person = Person.objects.get(id=id)
    serializer = PersonSerializer(person, many=False)
    return Response(serializer.data)

@api_view(["GET"])
def people(request) -> Response:
    person = Person.objects.all()
    serializer = PersonSerializer(person, many=True)
    return Response(serializer.data)