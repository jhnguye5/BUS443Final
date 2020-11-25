from django.db import models

class Studentdetails(models.Model):
    studentid = models.IntegerField()
    firstname = models.CharField(max_length=500)
    lastname = models.CharField(max_length=500)
    major = models.CharField(max_length=500)
    year = models.CharField(max_length=500)
    gpa = models.DecimalField(max_digits=3, decimal_places=2)

class Coursedetails(models.Model):
    courseid = models.IntegerField()
    coursetitle = models.CharField(max_length=500)
    coursename = models.CharField(max_length=500)
    coursesectioncode = models.IntegerField()
    coursedepartment = models.CharField(max_length=500)
    instructorfullname = models.CharField(max_length=500)
    
class Enrollment(models.Model):
    lastname = models.CharField(max_length=500)
    enrollment = models.CharField(max_length=500)
    
# Create your models here.
