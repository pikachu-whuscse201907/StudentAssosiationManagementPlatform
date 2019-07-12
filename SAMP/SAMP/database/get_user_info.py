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

#读取用户信息
def get_user_info(cookie_id):
	response = Person.objects.filter(cookie_id=cookie_id)
	if len(response)==0:#cookie_id不存在
		result={'success':False}
		result['notice']='The cookie_id is not exist.'
		return result
	elif cookie.cookie_create_time > response[0]['cookie_expire']:#cookie过期
		result={}
		result['success']=False
		result={'notice':'The cookie_id is out of date.'}
		return result
	else:#没问题则读取用户信息，放入result字典中
		user_info=User_Info.object.filter(name=response[0].name)
		result['gender']=user_info[0].gender
		result['motto']=user_info[0].motto
		result['birth_day']=user_info[0].birth_day
		return result