from rest_framework import serializers

from core.models import CustomUser, Education, Experiences, Project


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields: list[str] = [
            'id',
            'is_superuser',
            'email',
            'name',
            'first_name',
            'last_name',
            'about',
            'contact',
            'social_links',
            'blog'
        ]


class ExperienceSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Experiences
        fields: list[str] = [
            'id',
            'owner',
            'name',
            'role',
            'start_year',
            'end_year',
            'skill',
            'about_company'
        ]

    def get_owner(self, instance) -> str:
        ownerInstance: CustomUser = instance.owner
        return f"{ownerInstance.first_name} {ownerInstance.last_name}"
        # return {
        #     "name":ownerInstance.first_name,
        #     "lastName":ownerInstance.last_name,
        #     "email":ownerInstance.email,
        # }


class EducationSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Education
        fields: list[str] = [
            'id',
            'owner',
            'school_name',
            'start_year',
            'end_year',
            'degree',
            'course',
            'activities_societies'
        ]

    def get_owner(self, instance) -> str:
        ownerInstance: CustomUser = instance.owner
        return f"{ownerInstance.first_name} {ownerInstance.last_name}"


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Project
        exclude: list[str] = ['date_added', 'updated']

    def get_owner(self, instance) -> str:
        ownerInstance: CustomUser = instance.owner
        return f"{ownerInstance.first_name} {ownerInstance.last_name}"
