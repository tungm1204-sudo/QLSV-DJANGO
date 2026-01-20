from django.db import models

class Parent(models.Model):
    parent_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    dob = models.DateField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    mobile = models.CharField(max_length=15)
    status = models.BooleanField(default=True)
    last_login_date = models.DateField(blank=True, null=True)
    last_login_ip = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return f"{self.fname} {self.lname}"

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    dob = models.DateField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    parent = models.ForeignKey(Parent, on_delete=models.SET_NULL, null=True, blank=True)
    date_of_join = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=True)
    last_login_date = models.DateField(blank=True, null=True)
    last_login_ip = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return f"{self.fname} {self.lname}"
