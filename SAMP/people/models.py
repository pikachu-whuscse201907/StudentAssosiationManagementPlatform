# -*- coding: utf-8 -*-
from django.db import models
import os
import datetime


# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=30, null=False)
    pswd = models.CharField(max_length=256, null=False)
    cookie_id = models.CharField(max_length=256,null=True)
    cookie_create_time = models.DateTimeField(blank=True, null=True)
    cookie_expire = models.DateTimeField(blank=True, null=True)
    abc= models.CharField(max_length=100,null=True)

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
    name = models.OneToOneField(Person, on_delete=models.CASCADE)
    motto = models.CharField(max_length=100, default='')
    gender = models.IntegerField(choices=((0, "UNKNOWN"), (1, "MALE"), (2, "FEMALE")), default=0)
    birth_date = models.DateTimeField(null=True)
    profile = models.ImageField(upload_to=user_logo_path, null=False, default='default_user_logo.jpg')

    def __str__(self):
        return self.name.name


def org_logo_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format('org_logo_'+instance.organization_name, ext)
    ans = os.path.join("org_logo", instance.organization_name, filename)
    return ans
# Ending of function org_logo_path(instance, filename)


class ClubAnnouncements(models.Model):
    title = models.CharField(null=False, blank=False, max_length=20)
    create_date = models.DateTimeField(null=False, blank=False)
    content = models.CharField(null=False, blank=False, max_length=100)
    publisher = models.ForeignKey(User_info, null=True, related_name='clubannouncement_publisher',
                                  on_delete=models.SET_NULL)


# organization information
class Organizations(models.Model):
    create_status = models.IntegerField(choices=((0, "审核中"), (1, "已通过"), (2, "审核失败")),
                                        default=0)
    organization_name = models.CharField(primary_key=True, max_length=30, null=False)
    creator = models.ForeignKey(User_info, related_name='organization_creator',
                                on_delete=models.DO_NOTHING, blank=True)
    master = models.ForeignKey(User_info, related_name='organization_master',
                               on_delete=models.CASCADE, blank=True)
    members = models.ManyToManyField(User_info, related_name='organization_members', blank=True)
    description = models.CharField(max_length=1000, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    org_logo = models.ImageField(upload_to=org_logo_path, null=False,
                                 default='default_org_logo.jpg')
    announcements = models.ManyToManyField(ClubAnnouncements,
                                           related_name='organization_announcements',
                                           blank=True)
    
    def __str__(self):
        return self.organization_name


class MembershipApplication(models.Model):
    organization = models.ForeignKey(Organizations, related_name='membershipapplication_org',
                                     null=False, on_delete=models.DO_NOTHING)
    applicant = models.ForeignKey(User_info, related_name='membershipapplication_applicant',
                                  null=False, on_delete=models.DO_NOTHING)
    apply_message = models.CharField(max_length=100, default='')
    apply_time = models.DateTimeField(null=True, blank=True)
    application_status = models.IntegerField(choices=((0, "PENDING"), (1, "APPROVED"), (2, "DENIED"),
                                                      (3, "QUIT"), (4, "EXPELLED")), default=0)
    solver = models.ForeignKey(User_info, related_name='membershipapplication_solver',
                               null=True, blank=True, default=None, on_delete=models.DO_NOTHING)
    solve_time = models.DateTimeField(null=True, blank=True, default=None)
    reply_message = models.CharField(max_length=100, default='')
    
    inner_status_organization_exist = models.BooleanField(default=True)
    inner_status_applicant_exist = models.BooleanField(default=True)
    inner_status_solver_exist = models.BooleanField(default=True)
    # Inner status of a membership application.
    # If the record of the Organization is deleted (e.g. dismissed),
    # its attribute 'inner_status_organization_exist' should be set False,
    # and attribute 'organization' should NEVER be accessed again.
    # Same situation in case the record of the applicant or solver is deleted.
    
    def __str__(self):
        ans = ''
        ans += self.organization.organization_name
        ans += '-'
        ans += self.applicant.name.name
        ans += '-'
        if self.apply_time is not None:
            ans += self.apply_time.strftime('%Y-%m-%d %H:%M:%S')
            ans += '-'
        ans += self.apply_message
        return ans


class Activ(models.Model):
    organization = models.ForeignKey(Organizations,
                                     related_name='activ_organization',
                                     on_delete=models.CASCADE)
    activ_name = models.CharField(max_length=30, null=False)
    activ_time = models.DateTimeField(null=True, blank=True)
    activ_place = models.CharField(max_length=30, null=False)
    activ_content = models.CharField(max_length=300, null=False)
    activ_status = models.IntegerField(choices=((0, "审核中"), (1, "已通过"), (2, "审核失败")), default=0)

    def __str__(self):
        ans = ''
        ans += self.org_name.organization_name
        ans += '-'
        ans += self.activ_name
        return ans
