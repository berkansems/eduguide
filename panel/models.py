from django.contrib.auth.models import User
from django.db import models

class Branch(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=50)
    telephone = models.IntegerField()

    def __str__(self):
        return self.name



class Slider(models.Model):

    title = models.CharField(max_length=50)
    introduction = models.CharField(max_length=200)
    pic = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title

    def delete(self,*args,**kwargs):
        self.pic.delete()
        super().delete(*args,**kwargs)



class Courses(models.Model):
    branch = models.ForeignKey(Branch, related_name= "bra", null=True , on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, related_name= "teach" , null=True , on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    place = models.CharField(max_length=50)
    introduction = models.CharField(max_length=500)
    createdAt = models.DateTimeField(auto_now_add=True)
    startDate = models.CharField("Start Date (mm/dd/2020)",max_length=50)
    endDate = models.CharField("End Date (mm/dd/2020)",max_length=50)
    fee = models.IntegerField()
    capacity = models.IntegerField()
    pic = models.ImageField("Select an image file",null=True, blank=True)
    status=models.BooleanField("Active ?",default=True)

    def __str__(self):
        return self.branch.name + " : " + self.title

    def delete(self, *args, **kwargs):
        self.pic.delete()
        super().delete(*args, **kwargs)

    @property
    def statusChange(self):
        if self.status == True:
            self.status = False
        else:
            self.status = True
        return self.status

    @property
    def imageURL(self):
        try:
            url = self.pic.url
        except:
            url = ''
        return url


class Student(models.Model):
    Status = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected')
    )
    name=models.CharField(max_length=50)
    slugName = models.SlugField(max_length=200, null=True)
    email=models.EmailField()
    telephone=models.CharField(max_length=15)
    appDate=models.DateTimeField(auto_now_add=True)
    appStatus = models.CharField(max_length=50, null=True, choices=Status, default='Pending')
    course=models.ForeignKey(Courses,null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Admins(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    ip = models.CharField(max_length=200,null=True,blank=True)
    country = models.CharField(max_length=200,null=True)

class CronList(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=200, null=True, blank=True)
