from django.contrib import admin

# Register your models here.

from panel.models import Branch, Teacher, Courses, Student

class CoursesAdmin(admin.ModelAdmin):
    list_display = ('branch','teacher','place','fee','status')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name','email','telephone','course')

admin.site.register(Branch)
admin.site.register(Teacher)
admin.site.register(Courses,CoursesAdmin)
admin.site.register(Student,StudentAdmin)