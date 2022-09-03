from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
# Create your models here.

class Authentication(AbstractUser):
    username = models.CharField(max_length=100,primary_key=True)
    is_student = models.BooleanField(default = False)
    is_supervisor = models.BooleanField(default = False)
    mobile_number = models.CharField(max_length=10,unique=False,null = True)

class Hostel(models.Model):
    hostel_id = models.IntegerField(default=0,primary_key=True,null = False)
    hostel_name = models.CharField(max_length = 100)
    supervisor_mail = models.ForeignKey(to = Authentication,on_delete=models.CASCADE)
    floors = models.IntegerField(default=0)
    location = models.CharField(max_length=100)
    month_bill = models.IntegerField(default = 0)
    month_name = models.CharField(max_length = 20,default = '0')
    month_deadline = models.DateField(null = True,blank = True)

    def __str__(self):
        return str(self.hostel_id)

class Floor(models.Model):
    floor_id = models.IntegerField(default = 0)
    hostel_id = models.ForeignKey(to = Hostel,on_delete=models.CASCADE)
    no_of_rooms = models.IntegerField(default = 0)
    warden_name = models.CharField(max_length = 100)

    def __str__(self):
        return str(self.floor_id)

class Room(models.Model):
    room_id = models.IntegerField(default = 0,null = False)
    floor_id = models.ForeignKey(to = Floor,on_delete=models.CASCADE)
    hostel_id = models.ForeignKey(to = Hostel,on_delete=models.CASCADE)
    capacity = models.IntegerField(default = 0)
    no_of_students_occupied = models.IntegerField(default = 0)

class student_details(models.Model):
    student_mail = models.OneToOneField(Authentication,primary_key=True,null = False,on_delete=models.CASCADE)
    verified_by_supervisor = models.BooleanField(default = False)
    hostel_id =  models.ForeignKey(to = Hostel,on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20,unique=True,null=False)
    gender = models.CharField(max_length = 1)
    father_name = models.CharField(max_length = 100,null = False)
    mother_name = models.CharField(max_length = 100,null = False)
    parent_mobile_number = models.CharField(max_length = 10)
    date_of_birth = models.DateField()
    yos = models.IntegerField()
    course = models.CharField(max_length=100,null = False)
    address = models.CharField(max_length = 1024,null = False)
    assigned_room = models.IntegerField(default = -1)

class bill_payments(models.Model):
    student_email = models.OneToOneField(to = Authentication,on_delete=models.CASCADE,primary_key=True)
    applied_date = models.DateTimeField(auto_now_add = True)
    transaction_id = models.CharField(max_length = 100,blank = True,null = True)
    paid_date = models.DateField(null = True,blank = True)
    hostel_id = models.ForeignKey(to = Hostel,on_delete = models.CASCADE)
    payment_accepted = models.BooleanField(default = False)
    payment_paid = models.BooleanField(default = False)
    payment_rejected = models.BooleanField(default = False)
    transaction_image = models.ImageField(upload_to = "Transactions/",null = True,blank = True)

class Fines(models.Model):
    student_email = models.ForeignKey(to = Authentication,on_delete=models.CASCADE)
    hostel_id = models.ForeignKey(to = Hostel,on_delete = models.CASCADE)
    fine_month = models.CharField(max_length = 20)
    fine_amount = models.IntegerField()
    fine_deadline = models.DateField()
    date_created = models.DateField(auto_now=True)


