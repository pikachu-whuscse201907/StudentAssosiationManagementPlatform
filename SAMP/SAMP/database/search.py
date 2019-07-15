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
	if username is None:
		return False
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
	if _username is None:
		return None
	p = Person.objects.filter(name=_username)
	if len(p) == 0:
		return None
	else:
		return p[0]


def user_info_of_user(_user):
	if _user is None:
		return None
	p = User_info.objects.filter(name=_user)
	if len(p) == 0:
		return None
	else:
		return p[0]


def user_info_of_username(_username):
	if _username is None:
		return None
	user = user_of_username(_username)
	if user is None:
		return None
	user_info = user_info_of_user(user)
	return user_info


def user_of_cookie(_cookie_id):
	if _cookie_id is None:
		return None
	p = Person.objects.filter(cookie_id=_cookie_id)
	if len(p) == 0:
		return None
	elif expire(p[0].cookie_expire):
		return None
	else:
		return p[0]


def get_org_info(org_name):
	result = {}
	org_info = {}  # result字典中key 'org_info'对应的value
	response_1 = Organizations.objects.filter(organization_name=org_name)
	
	if 0 == len(response_1):
		result['success'] = False
		result['notice'] = 'No such organization.'
		result['org_info'] = org_info
		return result
	
	org_info['org_name'] = response_1[0].organization_name
	org_info['org_description'] = response_1[0].description
	org_info['create_date'] = response_1[0].create_date
	org_info['org_master'] = response_1[0].master.name.name
	org_info['creator'] = response_1[0].creator.name.name
	org_info['member_num'] = len(response_1[0].members.all())
	org_info['org_logo'] = response_1[0].org_logo
	
	result['success'] = True
	result['org_info'] = org_info
	return result



