from django.urls import path
from . import views


app_name = 'flyer'


urlpatterns = [
    path('', views.index, name='index'),
    path('editor/', views.editor, name='editor'),
    path('save_project/', views.save_project, name='save_project'),
    path('export_pdf/', views.export_pdf, name='export_pdf'),
]