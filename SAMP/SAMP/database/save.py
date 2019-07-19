from django.db import models
from people.models import Person, User_info, Organizations
from . import delete, search, save
import hashlib


def password_encrypt(pwd):#
	md5 = hashlib.md5() # 2,获取md5() 方法
	md5.update(pwd.encode()) # 3. 对字符串的字节类型加密
	result = md5.hexdigest() # 4.加密
	return result


# 存储注册设置的用户名和密码
def save_name_pswd(username, password1):
	User = Person.objects.create(name=username, pswd=password_encrypt(password1))
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
		save_cookie(response[0], cookie)
