# -*- coding: utf-8 -*-
from django.db import models
from ..view import *
from people.models import Person, User_info, Organizations
from ..Cookie import *
from .delete import delete_cookie
from .save import save_cookie




#修改用户信息
def update_user_info(cookie_id,info):
	response = Person.objects.filter(cookie_id=cookie_id)
	result = {}
	if len(response)==0:
		result['success']=False
		result['notice']='The cookie_id is not exist.'
		return result
	elif expire(response[0].cookie_expire):
		result['success']=False
		result['notice']='The cookie_id is out of date.'
		return result
	else:
		user_info_set = response[0].user_info_set.all()
		if 0<len(user_info_set):
			user_info=user_info_set[0]
		else:
			user_info = User_info.objects.create(name=response[0])
		user_info.gender = info['gender']
		user_info.motto = info['motto']
		user_info.birth_date = info['birth_date']
		user_info.save()

		result['success']=True
		return result


def save_default_user_info(username):
	cookie = Cookie()
	save_cookie(user_of_username(username), cookie)
	default_user_info = {'gender': 0, 'motto': '', 'birth_date': None}
	update_user_info(cookie.cookie_id, default_user_info)
	delete_cookie(cookie.cookie_id)


#查看用户信息
def get_user_info(cookie_id):
	response = Person.objects.filter(cookie_id=cookie_id)
	result = {}
	result['info'] = {}
	if len(response)==0:
		result['success']=False
		result['notice']='The cookie_id is not exist.'
		return result
	elif expire(response[0].cookie_expire):
		result['success']=False
		result['notice']='The cookie_id is out of date.'
		return result
	else:
		result['success']=True
		result['info']['user_name'] = response[0].name
		user_info_set = response[0].user_info_set.all()
		if 0 == len(user_info_set):
			save_default_user_info(response[0].name)
			result['info'] = {'gender': 0, 'motto': '', 'birth_date': None}
		else:
			user_info = User_info.objects.filter(name=response[0])
			result['info']['gender']=user_info[0].gender
			result['info']['motto']=user_info[0].motto
			result['info']['birth_date']=user_info[0].birth_date

		return result





#创建社团
def create_org(cookie_id, org_info):
	response = Person.objects.filter(cookie_id=cookie_id)
	result={}
	if len(response)==0:
		result['success']=False
		result['notice']='The cookie_id is not exist.'
		return result
	elif expire(response[0].cookie_expire):
		result['success']=False
		result['notice']='The cookie_id is out of date.'
		return result
	else:
		org=Organizations()
		result['success']=True
		get_org_info(org, org_info)
		return result





#搜索社团
def search_org(cookie_id, search_content):
	response = Person.objects.filter(cookie_id=cookie_id)
	result={}
	if len(response)==0:
		result['success']=False
		result['notice']='The cookie_id is not exist.'
		return result
	elif expire(response[0].cookie_expire):
		result={}
		result['success']=False
		result['notice']='The cookie_id is out of date.'
		return result
	else:
		result['success']=True
		org_info = Organizations.objects.filter(organization_name__icontains=search_content)
		org_list = {}
		org_list['id']=org_info.number
		org_list['organization_name']=org_info.organization_name
		org_list['creater']=org_info.creater
		org_list['number_of_members']=len(org_info.member)
		result['organizations']=org_list
		return result



#加入社团






#群主删除成员，提交群主的cookie_id
def delete_member(cookie_id, org_id):
	response = Person.objects.filter(cookie_id=cookie_id)
	result={}
	if len(response)==0:
		result['success']=False
		result['notice']='The cookie_id is not exist.'
		return result
	elif expire(response[0].cookie_expire):
		result['success']=False
		result['notice']='The cookie_id is out of date.'
		return result
	else:
		result['success']=True
		name=response[0]['name']
		members=Organizations.objects.filter(number=org_id)[0]['member']
		members.remove('name')




#成员退出社团，提交成员的cookie_id