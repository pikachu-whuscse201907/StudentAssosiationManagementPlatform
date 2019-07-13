from django.db import models
from ..view import *
from people.models import Person,User_info,Organizations
from ..Cookie import *
from .delete import *
from .search import user_of_username


# 存储注册设置的用户名和密码
def save_name_pswd(username, password1):
	User = Person.objects.create(name=username, pswd=password1)
	User.save()


# 用户登录时存储Cookie
def save_cookie(User,cookie):
	User.cookie_id=cookie.cookie_id
	User.cookie_expire=cookie.expire
	User.cookie_create_time=cookie.create_time
	User.save()


# 更新页面时，更新Cookie
def update_cookie(User, cookie):
	response = Person.objects.filter(cookie_id=cookie.cookie_id)
	if len(response) == 0:
		return False
	else:
		save_cookie(response[0],cookie)


#用户修改信息(除头像外），保存修改的信息
def modify_info(user_info, info):
	response = User_info.objects.filter(name=info.name)
	if len(response) == 0:
		return None
	else:
		user_info.name = info.name
		user_info.motto = info.name
		user_info.sex = info.sex
		user_info.birth_year = info.birth_year
		user_info.birth_month = info.birth_month
		user_info.birth_date = info.birth_date
		user_info.save()



#创立社团，填入信息
def get_org_info(org, info):
	if info.organization_name == None:
		return False
	else:
		org.number = info.number
		org.organization_name = info.organization_name
		org.creater = info.creater
		org.save()



