from rest_framework import serializers

from core.models import CustomUser, Education, Experiences, Person, Project

# ! REMOVE OWNER FOR ALL FIELDS IN PRODUCTION MODE

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude: list[str] = [
            'password',
            'is_active',
            'user_permissions',
            'groups',
            'date_joined',
            'is_staff',
            'last_login',
            'id'
            # ! REMOVE IS_SUPER WHEN YOU"RE INS PRODUCTION MODE BTW
        ]


class ExperienceSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Experiences
        exclude: list[str] = ['id']

    def get_owner(self, instance) -> str:
        ownerInstance: CustomUser = instance.owner
        return f"{ownerInstance.first_name} {ownerInstance.last_name}"


class EducationSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Education
        exclude = ['id']

    def get_owner(self, instance) -> str:
        ownerInstance: CustomUser = instance.owner
        return f"{ownerInstance.first_name} {ownerInstance.last_name}"


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Project
        exclude: list[str] = ['date_added', 'updated', 'id']

    def get_owner(self, instance) -> str:
        ownerInstance: CustomUser = instance.owner
        return f"{ownerInstance.first_name} {ownerInstance.last_name}"


class PersonSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    project = ProjectSerializer()
    experience = ExperienceSerializer()
    education = EducationSerializer()

    class Meta:
        model = Person
        fields = '__all__'

