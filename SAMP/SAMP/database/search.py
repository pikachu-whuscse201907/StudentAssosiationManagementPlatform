# -*- coding: utf-8 -*-
from django.db import models
from ..view import *
from people.models import Person
from ..Cookie import *
from .delete import *
from .save import *
from .search import *

# 查询用户注册/登录时输入的用户名是否已存在
def user_existing(username):
	response = Person.objects.filter(name=username)
	if len(response) == 0:
		return False    #该用户名不存在
	else:
		return True     #该用户名已存在


# 查询用户输入的密码是否与库中一致
def pswd_correct(username, password):
	User = Person.objects.filter(name=username)
	if len(User) == 0:
		return None
	else:
		if User[0].pswd == password:
			return User[0]   # 密码相同
		else:
			return None   # 密码不同，输入错误


def user_of_username(_username):
	p=Person.objects.filter(name=_username)
	if len(p) == 0:
		return None
	else:
		return p[0]


def user_of_cookie(_cookie_id):
	p=Person.objects.filter(cookie_id=_cookie_id)
	if len(p) == 0:
		return None
	elif expire(p[0].cookie_expire):
		return None
	else:
		return p[0]


#检查登录状态是否有效，None则为无效
def keep_visiting(cookie, User):
	response = Person.objects.values('cookie.cookie_expire').filter(cookie_id=cookie.cookie_id)
	if len(response)==0:
		return None
	else:
		if cookie.cookie_create_time <= response[0]['cookie_expire']:
			return User
		else:
			return None


