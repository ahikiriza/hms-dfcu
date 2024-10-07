# from datetime import datetime
from django.db import models
# from django.utils import timezone

# Create your models here.
# class Department(models.Model):
#     name = models.TextField() 
#     description = models.TextField() 
#     status = models.IntegerField() 
#     date_added = models.DateTimeField(default=timezone.now) 
#     date_updated = models.DateTimeField(auto_now=True) 

#     def __str__(self):
#         return self.name

# class Position(models.Model):
#     name = models.TextField() 
#     description = models.TextField() 
#     status = models.IntegerField() 
#     date_added = models.DateTimeField(default=timezone.now) 
#     date_updated = models.DateTimeField(auto_now=True) 

#     def __str__(self):
#         return self.name


# class Employees(models.Model):
#     code = models.CharField(max_length=100,blank=True) 
#     firstname = models.TextField() 
#     middlename = models.TextField(blank=True,null= True) 
#     lastname = models.TextField() 
#     gender = models.TextField(blank=True,null= True) 
#     dob = models.DateField(blank=True,null= True) 
#     contact = models.TextField() 
#     address = models.TextField() 
#     email = models.TextField() 
#     department_id = models.ForeignKey(Department, on_delete=models.CASCADE) 
#     position_id = models.ForeignKey(Position, on_delete=models.CASCADE) 
#     date_hired = models.DateField() 
#     salary = models.FloatField(default=0) 
#     status = models.IntegerField() 
#     date_added = models.DateTimeField(default=timezone.now) 
#     date_updated = models.DateTimeField(auto_now=True) 

#     def __str__(self):
#         return self.firstname + ' ' +self.middlename + ' '+self.lastname + ' '


# Create your models here.
class Staff(models.Model):
    employee_number = models.CharField(max_length=10, primary_key=True, unique=True)
    surname = models.CharField(max_length=100)
    other_names = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    id_photo = models.TextField(null=True, blank=True)  # Store Base64-encoded string
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.surname}, {self.other_names}"