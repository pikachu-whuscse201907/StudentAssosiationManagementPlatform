# -*- coding: utf-8 -*-
from django.db import models
from ..view import *
from people.models import Person
from ..Cookie import *
from .delete import *
from .save import *
from .search import *
from .update_user_info import *
from .get_user_info import  *

#存入用户信息
def update_user_info(cookie_id,info):
	response = Person.objects.filter(cookie_id=cookie_id)
	if len(response)==0:#如果cookie_id不存在
		result={}
		result['success']=False
		result['notice']='The cookie_id is not exist.'
		return result
	elif cookie.cookie_create_time > response[0]['cookie_expire']:#cookie过期
		result={}
		result['success']=False
		result={'notice':'The cookie_id is out of date.'}
		return result
	else:#没问题则录入用户信息
		user_info = User_Info.objects.filter(name=response[0].name)
		user_info.gender = info['gender']
		user_info.motto = info['motto']
		user_info.birth_day = info['birth_day']
		user.save()