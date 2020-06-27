from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from interface.forms import CreateUserForm
from interface.models import Customer
from panel.forms import StudentForm
from panel.models import Slider, Teacher, Branch, Courses, Student
from interface.decorators import unauthenticated_user




def index(request):
    teachers=Teacher.objects.all().count()
    branch=Branch.objects.all().count()
    course=Courses.objects.all().count()
    availables=Courses.objects.filter(status=True)
    recentCourses=availables.order_by('-pk')[:2]
    sliders=Slider.objects.all().order_by('-pk')[:5]
    studentsCount = Student.objects.all().count()

    context={'studentsCount':studentsCount,'sliders':sliders,'teachers':teachers,'branch':branch,'course':course,'recentCourses':recentCourses,'availables':availables}

    return render(request,'front/index.html',context)



@unauthenticated_user
def myLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        upass = request.POST.get('password')

        user = authenticate(username=username, password=upass)
        if user != None:
            login(request, user)
            return redirect('panel')
        else:

            messages.info(request, 'Username or password is incorrect')

    return render(request, 'front/login.html')

@unauthenticated_user
def mySignup(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form=CreateUserForm(request.POST)
        try:
            if form.is_valid():
                user = form.save()
                group = Group.objects.get(name='customer')
                user.groups.add(group)
                Customer.objects.create(
                   user=user,
                   name=user.username
                )
                return redirect('my_login')

        except:
            messages.info(request,{{form.errors}})
    context={'form':form}
    return render(request, 'front/signup.html',context)

def myLogout(request):
    logout(request)
    return redirect('home')



def order(request,pk):
    course=Courses.objects.get(id=pk)

    form=StudentForm()
    if request.method == "POST":
        form=StudentForm(request.POST)
        try:
            if form.is_valid():
                instance=form.save()
                instance.course=course
                instance.save()
                count=Student.objects.filter(course_id=pk).count()
                if count >= course.capacity:
                    course.status = False
                    course.save()

                messages.info(request,'You request for reservation applied successfully!')
        except:
            messages.info(request, 'Error occurred, please try again!')
        return redirect('order',pk)

    context={'course':course,'form':form}
    return render(request,'front/order.html',context)

