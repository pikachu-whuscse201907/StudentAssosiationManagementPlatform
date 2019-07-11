# -*- coding: utf-8 -*-
from django.db import models
from SAMP.view import *
from people.models import Person
from ..Cookie import *


#清空cookie_id
def delete_cookie_id(username):
    Person.objects.filter(name=username).update(cookie_id=None)


#清空expire time
def delete_cookie_expire(username):
    Person.objects.filter(name=username).update(cookie_expire=None)