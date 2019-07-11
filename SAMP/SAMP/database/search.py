# -*- coding: utf-8 -*-
from django.db import models
from SAMP.view import *
from people.models import Person
from ..Cookie import *


# 查询用户注册/登录时输入的用户名是否已存在
def user_existing(username):
	response = Person.objects.filter(name=username)
	if len(response) == 0:
		a=False    #该用户名不存在
	else:
		a=True    #该用户名已存在
	return a


# 查询用户输入的密码是否与库中一致
def pswd_correct(username, password):
	response = Person.objects.values('pswd').filter(name=username)
	if 0==len(response):
		return False
	if response[0]['pswd'] == password:
		a=True    #密码相同
	else:
		a=False    #密码不同，输入错误
	return a


# 查询cookie_id
def search_cookie_id(username):
	id_before = Person.objects.values('cookie_id').filter(name=username)
	return id_before


# 查询expire time
def search_cookie_expire(username):
	expire_time = Person.objects.values('cookie_expire').filter(name=username)
	return expire_time

