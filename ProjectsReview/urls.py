"""ProjectsReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from students import views
from django.contrib.auth import views as auth_views
admin.autodiscover()
urlpatterns = [
    path("",views.index,name="index"),
    path('student/',include('students.urls')),
    path('client/',include('clients.urls')),
    path('registration/',views.registration,name="registration"),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('admin/', admin.site.urls),
    path(r'project/<int:project_id>',views.project,name = 'project'),
    path('assign_preferences',views.assign_preferences,name = 'assign_preferences'),
    path('download/<str:filename>',views.download,name = 'download')
]