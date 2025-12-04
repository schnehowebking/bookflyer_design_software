import base64
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from .models import Project, FlyerTemplate
from .forms import ProjectForm
from reportlab.pdfgen import canvas
from io import BytesIO
from PIL import Image
import json




def index(request):
    templates = FlyerTemplate.objects.all()[:12]
    return render(request, 'flyer/index.html', {'templates': templates})

@login_required
def editor(request):
# basic editor page
    templates = FlyerTemplate.objects.all()[:12]
    return render(request, 'flyer/editor.html', {'templates': templates})


@csrf_exempt
@login_required
def save_project(request):
    if request.method == 'POST':
        name = request.POST.get('name', 'Untitled')
        json_data = request.POST.get('json_data', '')
        canvas_data = request.POST.get('canvas_data')
        project_id = request.POST.get('project_id')


        if project_id:
            project = Project.objects.get(pk=project_id, user=request.user)
        else:
            project = Project(user=request.user, name=name)


        project.json_data = json_data
        project.name = name


        if canvas_data:
        # canvas_data is expected like: data:image/png;base64,xxxx
            header, b64 = canvas_data.split(',', 1)
            file_data = ContentFile(base64.b64decode(b64), name=f'{name[:30]}.png')
            project.canvas_image.save(f'{name[:30]}.png', file_data, save=False)


        project.save()
        return JsonResponse({'status': 'ok', 'project_id': project.id})
    return JsonResponse({'status': 'failed'}, status=400)


@login_required
def export_pdf(request):
    # Accept an image or create PDF from JSON canvas
    canvas_img = request.GET.get('img') # base64 image data URL
    if not canvas_img:
        return HttpResponse('No image provided', status=400)


    header, b64 = canvas_img.split(',', 1)
    imgdata = base64.b64decode(b64)
    image = Image.open(BytesIO(imgdata)).convert('RGB')


    buffer = BytesIO()
    # create PDF with size matching image
    pdf = canvas.Canvas(buffer, pagesize=(image.width, image.height))
    # save image to temporary buffer
    img_buffer = BytesIO()
    image.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    pdf.drawInlineImage(Image.open(img_buffer), 0, 0, width=image.width, height=image.height)
    pdf.showPage()
    pdf.save()
    buffer.seek(0)


    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="flyer.pdf"'
    return response