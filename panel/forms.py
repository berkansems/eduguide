from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

class CreateAdminUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']