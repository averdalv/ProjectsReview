import random

from django.contrib.auth.models import AbstractUser
from django.core.files.storage import FileSystemStorage
from django.db import models

# Create your models here.
class User(AbstractUser):
    isClient = models.BooleanField(default=False)
    isStudent = models.BooleanField(default=False)
    def __str__(self):
        return self.username
class ProgrammingLuanguage(models.Model):
    name = models.CharField(max_length=100,blank=False)
    def __str__(self):
        return self.name
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    def __str__(self):
        return self.user.username
class Project(models.Model):
    name = models.CharField(max_length=200,blank=False)
    def __str__(self):
        return self.name
    acceptable_language = models.ManyToManyField(ProgrammingLuanguage)
    deadline = models.DateTimeField(blank=True)
    additional_requierements = models.CharField(max_length=400)
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    filename = models.FileField(blank=True)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    preference1 = models.ForeignKey(Project,null=True,on_delete=models.CASCADE, related_name='pref1')
    preference2 = models.ForeignKey(Project,null=True,on_delete=models.CASCADE, related_name='pref2')
    preference3 = models.ForeignKey(Project, null=True,on_delete=models.CASCADE, related_name='pref3')
    preference4 = models.ForeignKey(Project, null=True,on_delete=models.CASCADE, related_name='pref4')
    project_assigned = models.ForeignKey(Project, null=True,on_delete=models.SET_NULL, related_name='assignedProj')
    def __str__(self):
        return self.user.username



