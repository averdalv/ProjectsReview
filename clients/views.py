from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
# Create your views here.
from ProjectsReview import settings
from students.models import Client, ProgrammingLuanguage, Project


def add_project(request):
    if request.user.is_superuser or request.user.isClient:
        if request.method == 'GET':
            client = Client.objects.filter(user=request.user).first()
            languages = ProgrammingLuanguage.objects.all()
            context = {"client": client, "languages": languages}
            return render(request, 'addproject.html', context)
        if request.method == 'POST':
            name = request.POST['name']
            languages = request.POST.getlist('language')
            deadline = request.POST['deadline']
            additional_requirements = request.POST['additional_requierements']
            file = None
            if request.FILES.__contains__("file"):
                file = request.FILES['file']
            project = Project()
            client = Client.objects.filter(user=request.user).first()
            project.client = client
            project.name = name
            project.deadline = deadline
            project.additional_requierements = additional_requirements
            if file is not None:
                project.filename = file
            project.save()
            for language in languages:
                prog_lang = ProgrammingLuanguage.objects.filter(id = language).first()
                project.acceptable_language.add(prog_lang)
            project.save()
            projects = Project.objects.filter(client=client)
            context = {"projects": projects}
            return render(request, 'myprojects.html',context)
    else:
        context = {"error": True, "errorMessage": "You don't have permission to this page!"}
        return render(request, 'error.html', context)

def my_projects(request):
    if request.user.isClient:
        if request.method == 'GET':
            client = Client.objects.filter(user=request.user).first()
            projects = Project.objects.filter(client=client)
            context = {"projects":projects}
            return render(request,'myprojects.html',context)
    elif request.user.is_superuser:
        projects = Project.objects.all()
        context = {'projects':projects}
        return render(request, 'myprojects.html',context)

    else:
        context = {"error": True, "errorMessage": "You don't have permission to this page!"}
        return render(request, 'error.html', context)