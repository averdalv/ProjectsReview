from django.contrib import admin

# Register your models here.
from students.models import User, Student, Client, Project, ProgrammingLuanguage

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Client)
admin.site.register(Project)
admin.site.register(ProgrammingLuanguage)