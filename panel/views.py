import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.sessions.backends import file
from django.shortcuts import render, redirect
from django.http import HttpResponse

from panel.forms import CourseForm, SliderForm, CreateAdminUserForm
from panel.models import Branch, Teacher, Slider, Courses, Student, Admins
from .filters import OrderFilter
from panel.decorators import allowed_users, user_analysis
from ipware import get_client_ip
from ip2geotools.databases.noncommercial import DbIpCity
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required(login_url='my_login')
@user_analysis
def panel(request):
    count=Courses.objects.all().count()
    context={'count':count}
    ip, is_routable = get_client_ip(request)
    if ip is None:
        ip = "0.0.0.0"
    else:
        if is_routable:
            ipv = "Public"
        else:
            ipv = "Private"
    print(ip, ipv)
    return render(request, 'back/panel.html',context)

@login_required(login_url='my_login')
@allowed_users(allowed_roles=['admin'])
def branchAdd(request):
    if request.method == "POST":
        branchName = request.POST.get('name')

        if branchName == "":
            messages.info(request, 'please fill the required section')
            return redirect('branch_add')
        if len(Branch.objects.filter(name=branchName)) != 0:
            messages.info(request, 'this branch entered before, please try another branch name!')
            return redirect('branch_add')
        try:
            branch = Branch(name=branchName)
            branch.save()
        except:
            messages.info(request, 'please try again later!')
        return redirect('branch_list')
    return render(request, 'back/branch_add.html')

@login_required(login_url='my_login')
@allowed_users(allowed_roles=['admin'])
def branchList(request):
    branches = Branch.objects.all()
    context = {'branches': branches}
    return render(request, 'back/branch_list.html', context)

@login_required(login_url='my_login')
@allowed_users(allowed_roles=['admin'])
def branchDelete(request, pk):
    branch = Branch.objects.get(id=pk)
    branch.delete()
    return redirect('branch_list')

@login_required(login_url='my_login')
@allowed_users(allowed_roles=['admin'])
def branchUpdate(request, pk):
    branch = Branch.objects.get(id=pk)
    if request.method == "POST":
        try:
            branch.name=request.POST.get('name')
            branch.save()
        except:
            messages.info(request, 'please try again later!')
            return redirect('branch_update')
        return redirect('branch_list')

    return render(request, 'back/branch_update.html', {'branch': branch})
@login_required(login_url='my_login')
@allowed_users(allowed_roles=['admin'])
def courseAdd(request):
    teachers = Teacher.objects.all()
    branches=Branch.objects.all()
    form = CourseForm()
    if request.method == "POST":
        form = CourseForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('course_list')
        else:
            messages.info(request, 'Error occurred! try again!')
            return redirect('course_add')

    context = {"teachers": teachers, "branches": branches, "form":form}
    return render(request, 'back/course_add.html',context)

@login_required(login_url='my_login')
@allowed_users(allowed_roles=['admin'])
def courseList(request):
    courses = Courses.objects.all()

    paginator = Paginator(courses, 3)
    page = request.GET.get('page')
    try:
        courses = paginator.page(page)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        courses = paginator.page(1)

    context = {'courses': courses}
    return render(request, 'back/course_list.html',context)

def exportCatCsv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="category_list.csv"'
    writer = csv.writer(response)
    writer.writerow(['Title', 'Fee', 'Capacity', 'Status'])
    for i in Courses.objects.all() :
        writer.writerow([i.title, i.fee , i.capacity , i.status])
    return response

def importCatCsv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.info(request, "Please Input CSV File")
            return redirect('course_list')
        if csv_file.multiple_chunks():
            messages.info(request, "File too large")
            return redirect('course_list')

        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split("\n")
        for line in lines :

            fields = line.split(",")

            try:
                if len(Courses.objects.filter(title=fields[0])) == 0 and fields[0] != 'title' and fields[0] != '':
                    b = Courses(title=fields[0],fee=fields[1],capacity=fields[2],status=fields[3])
                    b.save()
            except:
                print("finish")
    return redirect('course_list')

@login_required(login_url='my_login')
@allowed_users(allowed_roles=['admin'])
def courseDelete(request,pk):
    course = Courses.objects.get(id=pk)
    course.delete()
    return redirect('course_list')

@login_required(login_url='my_login')
@allowed_users(allowed_roles=['admin'])
def courseStatusUpdate(request,pk):
    course = Courses.objects.get(id=pk)
    course.status = course.statusChange
    course.save()
    return redirect('course_list')

@login_required(login_url='my_login')
@allowed_users(allowed_roles=['admin'])
def courseUpdate(request,pk):
    teachers = Teacher.objects.all()
    branches = Branch.objects.all()
    course= Courses.objects.get(id=pk)
    form = CourseForm(instance=course)
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES,instance=course)

        if form.is_valid():

            form.save()

            return redirect('course_list')
        else:
            messages.info(request, 'Error occurred! try again!')
            return redirect('course_add')

    context = {"teachers": teachers, "branches": branches, "form": form}
    return render(request, 'back/course_update.html',context)

@login_required(login_url='my_login')
@allowed_users(allowed_roles=['admin'])
def sliderAdd(request):
    form = SliderForm()
    if request.method == "POST":
        form = SliderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('slider_list')
        else:
            messages.info(request, 'Error occurred! try again!')
            return redirect('slider_add')

    context = {'form':form}

    return render(request, 'back/slider_add.html',context)

@login_required(login_url='my_login')
@allowed_users(allowed_roles=['admin'])
def sliderList(request):
    sliders = Slider.objects.all()
    context = {'sliders': sliders}

    return render(request, 'back/slider_list.html',context)


def sliderDelete(request,pk):
    slider = Slider.objects.get(id=pk)
    slider.delete()
    return redirect('slider_list')


@login_required(login_url='my_login')
@allowed_users(allowed_roles=['admin'])
def sliderUpdate(request,pk):
    slider = Slider.objects.get(id=pk)
    form = SliderForm(instance=slider)
    if request.method == "POST":
        form = SliderForm(request.POST, request.FILES,instance=slider)
        if form.is_valid():
            form.save()
            return redirect('slider_list')
        else:
            messages.info(request, 'Error occurred! try again!')
            return redirect('slider_add')

    context = {'form': form}

    return render(request, 'back/slider_update.html', context)



@login_required(login_url='my_login')
@allowed_users(allowed_roles=['admin'])
def teacherAdd(request):
    if request.method == "POST":
        teacherName = request.POST.get('name')
        teacherTelephone = request.POST.get('telephone')

        if teacherName == "" or teacherTelephone == "":
            messages.info(request, 'please fill the required sections')
            return redirect('teacher_add')

        if len(Teacher.objects.filter(name=teacherName)) != 0 and len(
                Teacher.objects.filter(telephone=teacherTelephone)) != 0:
            messages.info(request, 'this branch entered before with the same phone number!')
            return redirect('teacher_add')

        try:
            teacher = Teacher(name=teacherName, telephone=teacherTelephone)
            teacher.save()
        except:
            messages.info(request, 'Error occurred! please try again!')
            messages.info(request, 'Telephone number must be integer!')
            return redirect('teacher_add')
        return redirect('teacher_list')

    return render(request, 'back/teacher_add.html')

@login_required(login_url='my_login')
@allowed_users(allowed_roles=['admin'])
def teacherList(request):
    teachers = Teacher.objects.all()
    context = {'teachers': teachers}
    return render(request, 'back/teacher_list.html', context)

@login_required(login_url='my_login')
@allowed_users(allowed_roles=['admin'])
def teacherDelete(request, pk):
    teacher = Teacher.objects.get(id=pk)
    teacher.delete()
    return redirect('teacher_list')

@login_required(login_url='my_login')
@allowed_users(allowed_roles=['admin'])
def teacherUpdate(request, pk):
    teacher = Teacher.objects.get(id=pk)
    if request.method == "POST":
        try:
            teacher.name = request.POST.get('name')
            teacher.telephone = request.POST.get('telephone')
            teacher.save()
        except:
            messages.info(request, 'please try again later!')
            messages.info(request, 'Telephone number must be integer!')
            return redirect('teacher_update')
        return redirect('teacher_list')

    return render(request, 'back/teacher_update.html', {'teacher': teacher})

@login_required(login_url='my_login')
@allowed_users(allowed_roles=['admin'])
def applies(request):

    myFilter = OrderFilter(request.GET)
    students = myFilter.qs
    context={'students':students,'myFilter':myFilter}
    return render(request, 'back/applies.html', context)


@login_required(login_url='my_login')
@allowed_users(allowed_roles=['admin'])
def studentStatusAccept(request,pk):
    student=Student.objects.get(id=pk)
    student.appStatus= 'Accepted'
    student.save()
    return redirect('applies')

@login_required(login_url='my_login')
@allowed_users(allowed_roles=['admin'])
def studentStatusReject(request,pk):
    student = Student.objects.get(id=pk)
    student.appStatus = 'Rejected'
    student.save()
    return redirect('applies')

@login_required(login_url='my_login')
def studentStatusPending(request,pk):
    student = Student.objects.get(id=pk)
    student.appStatus = 'Pending'
    student.save()
    return redirect('applies')



@login_required(login_url='my_login')
@allowed_users(allowed_roles=['admin'])
def adminAdd(request):
    form = CreateAdminUserForm(request.POST)
    if request.method == "POST":
        try:
            if form.is_valid():
                user = form.save()

                group = Group.objects.get(name='admin')
                user.groups.add(group)
                ip, is_routable = get_client_ip(request)
                if ip is None:
                    ip = "0.0.0.0"
                try:
                    response= DbIpCity.get(ip,api_key='free')
                    country = response.country + " | " + response.city
                except:
                    country="Unknown"
                Admins.objects.create(
                    user=user,
                    name=user.username,
                    ip = ip,
                    country = country,
                )
                return redirect('admin_list')

        except:
            messages.info(request,'Errors found')
    context = {'form':form}
    return render(request,'back/admin_add.html',context)

@login_required(login_url='my_login')
@allowed_users(allowed_roles=['admin'])
def adminList(request):
    adminUsers=Admins.objects.all().exclude(user=request.user.is_staff)
    context={'adminUsers':adminUsers}
    return render(request,'back/admin_list.html',context)

@login_required(login_url='my_login')
@allowed_users(allowed_roles=['admin'])
def adminDelete(request,pk):
    adminUser=Admins.objects.get(id=pk)
    if request.user.is_staff:
        adminUser.delete()
    else:
        messages.info(request,'Only superusers(staffs) can delete admins!')
    return redirect('admin_list')