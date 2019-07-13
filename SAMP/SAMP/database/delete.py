# -*- coding: utf-8 -*-
from django.db import models
from ..view import *
from people.models import Person,User_info,Organizations
from ..Cookie import *
from .delete import *
from .save import *
from .search import *


# 退出登录，清空Cookie
def delete_cookie(_cookie_id):
	response = Person.objects.filter(cookie_id=_cookie_id)
	if len(response)==0:
		return False
	else:
		clear_cookie(response[0])
		return True


def clear_cookie(User):
	User.cookie_id=None
	User.cookie_create_time=None
	User.cookie_expire=None
	User.save()
