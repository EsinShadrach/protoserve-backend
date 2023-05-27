from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.utils import timezone


YEAR_CHOICES:list[tuple[str | str]] = [
    (str(year), str(year)) for year in range(1950, 2100)
]

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        email: str = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30, blank=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    about = models.TextField(blank=True)
    contact = models.JSONField(default=dict)
    social_links = models.JSONField(default=list)
    skills = models.JSONField(default=list)
    intro_text = models.CharField(max_length=200, blank=True)
    blog = models.CharField(max_length=150, blank=True)
    # TODO: ADD PROFILE PIC FIELD HERE
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS: list[str] = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name_plural: str = 'Custom users'


class Experiences(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=100)
    start_year = models.CharField(max_length=4, choices=YEAR_CHOICES)
    end_year = models.CharField(max_length=4, blank=True, choices=YEAR_CHOICES)
    skill = models.JSONField(default=list,)
    about_company = models.TextField(max_length=250)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural: str = "Experiences"


class Education(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    school_name = models.CharField(max_length=150)
    start_year = models.CharField(max_length=4, choices=YEAR_CHOICES)
    end_year = models.CharField(max_length=4, blank=True, choices=YEAR_CHOICES)
    degree = models.CharField(max_length=200)
    course = models.CharField(max_length=200)
    activities_societies = models.JSONField(default=list, blank=True, null=True)

    def __str__(self) -> str:
        return self.school_name

    class Meta:
        verbose_name_plural: str = "Educations"


class Project(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=250)
    live_preview = models.CharField(max_length=300, blank=True, null=True)
    repository = models.CharField(max_length=200)
    # TODO: projectMedia = "" ADD PROJECT MEDIA HERE
    about_project = models.TextField(max_length=300)
    tools = models.JSONField(default=list)
    year = models.CharField(max_length=4, blank=True, choices=YEAR_CHOICES)
    category = models.JSONField(default=list, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.project_name

    class Meta:
        verbose_name_plural: str = "Projects"
        ordering: list[str] = ['-updated', '-date_added']
