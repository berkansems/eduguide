from django.contrib import admin

# Register your models here.

from panel.models import Branch, Teacher, Courses, Student

admin.site.register(Branch)
admin.site.register(Teacher)
admin.site.register(Courses)
admin.site.register(Student)