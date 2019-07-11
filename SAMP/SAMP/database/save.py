# -*- coding: utf-8 -*-
from django.db import models
from SAMP.view import *
from people.models import Person
from ..Cookie import *


# 存储注册设置的用户名和密码
def save_name_pswd(username, password1):
    test = Person(name=username, pswd=password1)
    test.save()


# 存储cookie_id
def save_cookie_id(cookie_id, username):
    Person.objects.filter(name=username).update(cookie_id=cookie_id)


# 存储expire time
def save_cookie_expire(username, expire):
    Person.objects.filter(name=username).update(cookie_expire=expire)
