# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=30,null=False)
    pswd = models.CharField(max_length=256,null=False)
    cookie_id = models.CharField(max_length=256,null=True)
    cookie_create_time = models.DateTimeField(blank=True,null=True)
    cookie_expire=models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.name

#personal information
class User_info(models.Model):
    name = models.ForeignKey(Person,'on_delete=models.CASCADE()')
    motto = models.CharField(max_length=100)
    sex = models.IntegerField(choices=((1, "男"), (2, "女")), default=1)
    birth_year = models.IntegerField(default=2019)
    birth_month = models.SmallIntegerField(default=12)
    birth_date = models.DateField()
    profile = models.ImageField()

    def __str__(self):
        return self.name

#organization information
class organizations(models.Model):
    number = models.BigAutoField(primary_key=True)
    organization_name = models.CharField(max_length=30,null=False)
    creater = models.CharField(max_length=30)
    manager =  models.CharField(max_length=30)
    member =  models.CharField(max_length=30)

    def __str__(self):
        return self.number