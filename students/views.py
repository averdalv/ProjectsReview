from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from ProjectsReview import settings
from students.models import Student, Client, User, Project, ProgrammingLuanguage
from students.project_preferences import generate_project_preferences


def registration(request):
    if request.method == 'GET':
        return render(request, 'registration.html')
    if request.method== 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        radio = request.POST["radio"]
        email = request.POST["email"]
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        u = User.objects.filter(username=username).first()
        if u is not None:
            context = {"error":True,"errorMessage":"User with such username already exists!"}
            return render(request,"registration.html",context)
        u = User.objects.filter(email=email).first()
        if u is not None:
            context = {"error":True,"errorMessage":"User with such email already exists!"}
            return render(request,"registration.html",context)
        user = User.objects.create_user(username, email, password,last_name=last_name,first_name=first_name)
        print("type: ",type(radio))
        if radio=="student":
            user.isStudent = True
            user_model = Student.objects.create(user=user)
        else:
            user.isClient = True
            user_model = Client.objects.create(user=user)
        user.save()
        user_model.save()
        login(request,user)
        return render(request, 'index.html')
def login_user(request):
    if request.method== 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username,password=password)
        if user is None:
            context = {"error": True, "errorMessage": "Wrong username or password!"}
            return render(request,'error.html',context)
        else:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request,user)
            if user.isClient:
                return render(request,'index.html')
            if user.isStudent:
                return render(request, 'index.html')
            if user.is_superuser:
                return HttpResponseRedirect("/admin/")


def logout_user(request):
    logout(request)
    return render(request, 'index.html')


def index(request):
    return render(request, 'index.html')


def projects(request):
    if request.user.is_superuser or request.user.isStudent:
        projects_list = Project.objects.all()
        context = {"projects":projects_list}
        return render(request, 'projects.html',context)
    else:
        context = {"error": True, "errorMessage": "You don't have permission to this page!"}
        return render(request, 'error.html', context)


def project(request, project_id):
    proj = Project.objects.filter(id=project_id).first()
    if request.user.isClient:
        client = Client.objects.filter(user=request.user).first()
        if proj.client != client:
            return render(request, 'error.html', context={"error": True, "errorMessage": "You don't have permission to this page!"})
    students = Student.objects.filter(project_assigned=proj).all()
    acceptable_languages = proj.acceptable_language.all()
    context = {"project":proj,"acceptable_languages":acceptable_languages}
    if students is not None:
        context["students"] = students
    return render(request,"project.html",context)


def project_preferences(request):
    if request.user.is_superuser or request.user.isStudent:
        if request.method=="GET":
            student = Student.objects.filter(user=request.user).first()
            projects = Project.objects.all()
            context = {"student":student,"projects":projects}
            return render(request,"preferences.html",context)
        if request.method == "POST":
            if len(Project.objects.all()) == 0:
                return render(request, 'error.html',
                              context={"error": True,
                                       "errorMessage": "System doesn't contain projects right now!"})
            student = Student.objects.filter(user=request.user).first()
            preference1 = request.POST["pref1"]
            preference2 = request.POST["pref2"]
            preference3 = request.POST["pref3"]
            preference4 = request.POST["pref4"]
            student.preference1 = Project.objects.filter(id=preference1).first()
            student.preference2 = Project.objects.filter(id=preference2).first()
            student.preference3 = Project.objects.filter(id=preference3).first()
            student.preference4 = Project.objects.filter(id=preference4).first()
            student.save()
            projects_list = Project.objects.all()
            context = {"projects": projects_list}
            return render(request, "projects.html",context)
    else:
        return render(request, 'error.html',
                      context={"error": True, "errorMessage": "You don't have permission to this page!"})


def assign_preferences(request):
    if request.user.is_superuser:
        try:
            list_result = generate_project_preferences()
            context = {"list_result":list_result}
            return render(request,"assignments.html",context)
        except:
            return render(request, 'error.html',
                          context={"error": True, "errorMessage": "System is not properly filled to assign students!"})
    else:
        return render(request, 'error.html',
                      context={"error": True, "errorMessage": "You don't have permission to this page!"})


def download(request,filename):
    path = settings.MEDIA_ROOT+'\\'+filename
    f = open(path, 'r')
    response = HttpResponse(f, content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename='+filename
    return response