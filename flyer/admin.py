from django.contrib import admin
from .models import FlyerTemplate, Project


@admin.register(FlyerTemplate)
class FlyerTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'updated_at')