from django.contrib import admin

from core.models import CustomUser, Experiences, Project, Education

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Experiences)
admin.site.register(Education)
admin.site.register(Project)