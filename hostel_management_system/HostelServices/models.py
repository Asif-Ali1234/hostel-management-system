from django.db import models
from Accounts.models import Authentication
# Create your models here.

class student_leaves(models.Model):
    student_email = models.ForeignKey(to = Authentication,on_delete = models.CASCADE)
    applied_date = models.DateTimeField(auto_now=True)
    startdate = models.DateField()
    enddate = models.DateField()
    reason = models.TextField()
    is_accepted = models.BooleanField(default = False)
    is_rejected = models.BooleanField(default = False)
    allow_new_leave = models.BooleanField(default = True)

class student_grievances(models.Model):
    student_email = models.ForeignKey(to = Authentication,on_delete=models.CASCADE)
    applied_date = models.DateTimeField(auto_now=True)
    grievance = models.TextField()
    is_accepted = models.BooleanField(default = False)
    is_rejected = models.BooleanField(default = False)
    is_completed = models.BooleanField(default = False)




