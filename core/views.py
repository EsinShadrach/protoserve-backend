from django.db.models import Q
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response


from core.models import CustomUser, Education, Experiences, Project
from core.serializers import (
    EducationSerializer,
    ExperienceSerializer,
    ProjectSerializer,
    UserSerializer
)

# Create your views here.

# ! YOU SHOULD ONLY BE ABLE TO SEE YOUR OWN DATA SO RESTRICTED VIEWS


@api_view(['GET'])
def endpoints(request) -> Response:
    link = 'http://127.0.0.1:8000'
    endpoint_list: list[str] = [
        f'{link}/educations/',
        '/education/:school_name',

        f'{link}/experiences',
        '/experiences/:name',

        f'{link}/projects',
        '/projects/:project_name',

        # ! PEOPLE WOULD BE HIDDEN BUT NOT `PERSON`
        # ! IMPLEMENT PERSON FIELD LATER
        # ! USER WOULD BE HIDDEN
        f'{link}/users',
        '/user/:first_name'
    ]
    return Response(endpoint_list)


@api_view(['GET', 'POST'])
def users(request) -> Response:
    if request.method == "GET":
        query = request.GET.get('query', '')

        users = CustomUser.objects.filter(
            Q(name__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=200)

    if request.method == "POST":
        user_data = request.data.copy()
        user_data['is_superuser'] = False
        user_data['name'] = f"{user_data['first_name']} {user_data['last_name']}"

        user = CustomUser.objects.create_user(**user_data)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)


@api_view(['GET', 'PUT', 'DELETE'])
def userDetailed(request, first_name) -> Response:
    try:
        user: CustomUser = CustomUser.objects.get(first_name=first_name)
    except CustomUser.DoesNotExist:
        return Response({'detail': f'{first_name} not found'}, status=404)

    if request.method == "GET":
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    if request.method == "DELETE":
        user.delete()
        return Response({'detail': f'{first_name} deleted'}, status=204)


@api_view(["POST", "GET"])
@permission_classes([IsAdminUser])
def superusers(request) -> Response:
    if request.method == "GET":
        query = request.GET.get('query', '')
        users = CustomUser.objects.filter(
            Q(name__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) &
            Q(is_superuser=True)
        )

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        user_data = request.data.copy()
        user_data['is_superuser'] = True
        user_data['name'] = f"{user_data['first_name']} {user_data['last_name']}"

        user = CustomUser.objects.create_user(**user_data)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)


@api_view(["GET", "POST"])
def experiences(request) -> Response:
    if request.method == "GET":
        query: str = request.GET.get("query", "")

        experiences = Experiences.objects.filter(
            Q(name__icontains=query) |
            Q(role__icontains=query) |
            Q(start_year__icontains=query) |
            Q(skill__icontains=query)
        )

        serializer = ExperienceSerializer(experiences, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        user_data = request.data.copy()
        user_data['owner'] = request.user

        experience = Experiences.objects.create(**user_data)

        serializer = ExperienceSerializer(experience, many=False)
        return Response(serializer.data)


@api_view(["GET", "PUT", "DELETE"])  # ! ADDING ABILITY TO GET PUT AND DELETE
def experiencesDetails(request, name) -> Response:
    try:
        experiences: Experiences = Experiences.objects.get(name=name)
    except Experiences.DoesNotExist:
        return Response({'detail': f'{name} not found'}, status=404)

    if request.method == "GET":
        serializer = ExperienceSerializer(experiences, many=False)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = ExperienceSerializer(
            experiences, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    if request.method == "DELETE":
        experiences.delete()
        return Response({'detail': f'{name} deleted'}, status=204)


@api_view(["GET", "POST"])
def education(request) -> Response:
    if request.method == "GET":
        query: str = request.GET.get("query", '')

        education = Education.objects.filter(
            Q(school_name__icontains=query) |
            Q(start_year__icontains=query) |
            Q(degree__icontains=query)
        )
        serializer = EducationSerializer(education, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        user_data = request.data.copy()
        user_data['owner'] = request.user

        education = Education.objects.create(**user_data)

        serializer = EducationSerializer(education, many=False)
        return Response(serializer.data)


@api_view(["GET", "PUT", "DELETE"])
def educationDetails(request, school_name) -> Response | None:
    try:
        education: Education = Education.objects.get(school_name=school_name)
    except Education.DoesNotExist:
        return Response({'detail': f'{school_name} not found'}, status=404)

    if request.method == "GET":
        serializer = EducationSerializer(experiences, many=False)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = EducationSerializer(
            education, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    if request.method == "DELETE":
        education.delete()
        return Response({'detail': f'{school_name} deleted'}, status=204)


@api_view(["GET", "POST"])
def project(request) -> Response | None:
    if request.method == "GET":
        query: str = request.GET.get("query", '')

        project = Project.objects.filter(
            Q(project_name__icontains=query) |
            Q(tools__icontains=query) |
            Q(about_project__icontains=query) |
            Q(year__icontains=query) |
            Q(category__icontains=query)
        )
        serializer = ProjectSerializer(project, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        user_data = request.data.copy()
        user_data['owner'] = request.user

        project = Project.objects.create(**user_data)

        serializer = ProjectSerializer(project, many=False)
        return Response(serializer.data)


@api_view(["GET", "PUT", "DELETE"])
def projectDetailed(request, project_name) -> Response:
    try:
        project: Project = Project.objects.get(project_name=project_name)
    except Project.DoesNotExist:
        return Response({'detail': f'{project_name} not found'}, status=404)

    if request.method == "GET":
        serializer = ProjectSerializer(project, many=False)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = ProjectSerializer(
            project, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    if request.method == "DELETE":
        project.delete()
        return Response({'detail': f'{project_name} deleted'}, status=204)
