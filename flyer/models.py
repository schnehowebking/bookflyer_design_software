from django.db import models
from django.contrib.auth.models import User


class FlyerTemplate(models.Model):
    name = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to='templates/thumbnails/', blank=True, null=True)
    json_layout = models.TextField(help_text='JSON describing layout positions etc.', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


def __str__(self):
    return self.name




class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to='projects/covers/', blank=True, null=True)
    canvas_image = models.ImageField(upload_to='projects/canvas/', blank=True, null=True)
    json_data = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def __str__(self):
    return self.name