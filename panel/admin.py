from django.contrib import admin

# Register your models here.

from panel.models import Branch, Teacher, Courses, Student

class CoursesAdmin(admin.ModelAdmin):
    list_display = ('branch','teacher','place','fee','status')
    list_filter = ('status','fee',)
    search_fields = ('teacher',)
    ordering = ('fee',)
    raw_id_fields = ('teacher',) # liste çıkarmıyor sadece id veriyor



class StudentAdmin(admin.ModelAdmin):
    list_display = ('name','email','telephone','course')# extra fields in the admin
    list_filter = ('appStatus','course') #filters
    search_fields = ('name','email',) #bu alanlar üzerinde search yapılacaktır
    date_hierarchy = 'appDate' #navigate quickly through a date hierarchy.
    ordering = ['appStatus','appDate'] #order the list by 'appStatus' and then 'appDate'
    prepopulated_fields = {'slugName': ('name',)} # write slug of the given name automatically


admin.site.register(Branch)
admin.site.register(Teacher)
admin.site.register(Courses,CoursesAdmin)
admin.site.register(Student,StudentAdmin)