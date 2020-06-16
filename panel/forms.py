from django import forms

from panel.models import Courses, Slider,Student


class CourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = '__all__'

class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = '__all__'

class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields= ['name','email', 'telephone']

