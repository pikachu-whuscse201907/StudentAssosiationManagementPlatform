# -*- coding: utf-8 -*-
from django.db import models
import os


# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=30,null=False)
    pswd = models.CharField(max_length=256,null=False)
    cookie_id = models.CharField(max_length=256,null=True)
    cookie_create_time = models.DateTimeField(blank=True,null=True)
    cookie_expire = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.name


def user_logo_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format('user_logo_'+instance.name.name, ext)
    # return the whole path to the file
    ans = os.path.join("user_logo", instance.name.name, filename)
    return ans
# Ending of function user_logo_path(instance, filename)


# personal information
class User_info(models.Model):
    name = models.OneToOneField(Person, on_delete = models.CASCADE)
    motto = models.CharField(max_length = 100)
    gender = models.IntegerField(choices = ((0, "unknow"), (1, "male"), (2, "female")), default=0)
    birth_date = models.DateTimeField(null = True)
    profile = models.ImageField(upload_to = user_logo_path, null = True)

    def __str__(self):
        return self.name


def org_logo_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format('org_logo_'+instance.organization_name, ext)
    ans = os.path.join("org_logo", instance.organization_name, filename)
    return ans
# Ending of function org_logo_path(instance, filename)


class ClubPronounces(models.Model):
    title = models.CharField(null=False, blank=False, max_length=20)
    create_date = models.DateTimeField(null=False, blank=False)
    content = models.CharField(null=False, blank=False, max_length=100)
    
    
# organization information
class Organizations(models.Model):
    organization_name = models.CharField(primary_key=True,max_length=30, null=False)
    creator = models.ForeignKey(User_info, related_name='organization_creator', on_delete=models.DO_NOTHING)
    master = models.ForeignKey(User_info, related_name='organization_master', on_delete=models.CASCADE)
    members = models.ManyToManyField(User_info, related_name='organization_members')
    description = models.CharField(max_length=1000, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    org_logo = models.ImageField(upload_to=org_logo_path, null=True)
    pronounces = models.ManyToManyField(ClubPronounces, related_name='organization_pronounces')
    
    def __str__(self):
        return self.organization_name
