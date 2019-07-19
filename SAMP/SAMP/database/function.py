# -*- coding: utf-8 -*-
from django.db import models
import datetime
from people.models import Person, User_info, Organizations, ClubAnnouncements, MembershipApplication,Activ
from ..Cookie import *
from . import delete
from .save import save_cookie
from .search import user_of_username
import PIL.Image


# 修改用户信息
def update_user_info(cookie_id, info):
    response = Person.objects.filter(cookie_id=cookie_id)
    result = {}
    if len(response)==0:
        result['success'] = False
        result['notice'] = 'The cookie_id is not exist.'
        return result
    elif expire(response[0].cookie_expire):
        result['success'] = False
        result['notice'] = 'The cookie_id is out of date.'
        return result
    else:
        user_info_set = User_info.objects.filter(name=response[0])
        if 0 < len(user_info_set):
            user_info = user_info_set[0]
        else:
            user_info = User_info.objects.create(name=response[0])
        user_info.gender = info['gender']
        user_info.motto = info['motto']
        if 'birth_date' in info.keys():
            user_info.birth_date = info['birth_date']
        if 'user_logo' in info.keys():
            user_info.profile = info['user_logo']
        
        user_info.save()
        
        result['success'] = True
        return result
# Ending of function update_user_info(cookie_id, info)


def save_default_user_info(username):
    cookie = Cookie()
    save_cookie(user_of_username(username), cookie)
    
    default_user_info = {'gender': 0, 'motto': '', 'birth_date': None}
    update_user_info(cookie.cookie_id, default_user_info)
    delete.delete_cookie(cookie.cookie_id)
# Ending of function save_default_user_info(username)


# 查看用户信息
def get_user_info(cookie_id):
    result = {}
    if cookie_id is None:
        result['success']=False
        return result
    response = Person.objects.filter(cookie_id=cookie_id)
    result['info'] = {}
    if len(response)==0:
        result['success']=False
        result['notice']='The cookie_id is not exist.'
        return result
    elif expire(response[0].cookie_expire):
        delete.delete_cookie(cookie_id)
        result['success']=False
        result['notice']='The cookie_id is out of date.'
        return result
    else:
        result['success']=True
        result['info']['user_name'] = response[0].name
        user_info_set = User_info.objects.filter(name=response[0])
        if 0 == len(user_info_set):
            save_default_user_info(response[0].name)
            result['info'] = {'gender': 0, 'motto': '', 'birth_date': None}
        else:
            user_info = User_info.objects.filter(name=response[0])
            result['info']['gender'] = user_info[0].gender
            result['info']['motto'] = user_info[0].motto
            result['info']['birth_date'] = user_info[0].birth_date
            result['info']['user_logo'] = user_info[0].profile
        
        return result
# Ending of function get_user_info(cookie_id)


# 创建社团
def create_org(cookie_id, creator, org_name, org_description, img):
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

    org_info = Organizations.objects.filter(organization_name=org_name)
    if len(org_info)!=0:
        result['success']=False
        result['notice']='The organization name has been used.'
        return result

    if response[0].name != creator:
        result['success']=False
        result['notice']='{0} haven\'t log in! Please log in first!'.format(creator)
        return result
    user_info = User_info.objects.get(name=response[0])
    org_create = Organizations.objects.create(organization_name=org_name, description=org_description, master=user_info, creator=user_info, org_logo=img)
    # org_create.create_data=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    org_create.description = org_description
    org_create.create_date = datetime.datetime.now()
    org_create.members.add(user_info)
    org_create.save()
    result['success'] = True
    return result
# Ending of function create_org(cookie_id, creator, org_name, org_description, img)


# 搜索社团
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
        org_info = Organizations.objects.filter(organization_name__icontains=search_content,
                                                create_status=1)
        org_list = []
        for each in org_info:
            org_list.append((each.organization_name, each.description))
        result['org_list'] = org_list
        result['success'] = True
        return result
# Ending of function search_org(cookie_id, search_content)


# 成员申请加入社团，提交成员的cookie_id，生成新的MemberApplication对象
def join_org(cookie_id, org_name):
    response = Person.objects.filter(cookie_id=cookie_id)
    result={}
    result['success']=False
    if len(response)==0:  # 如果cookie不存在，加入失败
        result['notice']='The cookie_id does not exist.'
        return result
    elif expire(response[0].cookie_expire):  # 如果cookie过期，加入失败
        result['notice']='The cookie_id is out of date.'
        return result

    response_1 = Organizations.objects.filter(organization_name=org_name, create_status=1)  # 获取该社团信息
    user_info = response[0].user_info
    if len(response_1) == 0:  # 该社团不存在，加入失败
        result['notice']='The organization does not exist.'
        return result
    org = response_1[0]
    
    # 根据输入是社团id,查看社团成员列表member(连接到User_info表），如果该社团存在，则加入失败
    members = org.members.all()
    if user_info in list(members):
        result['notice']='You are already in this club.'
        return result
    
    applications = MembershipApplication.objects.filter(organization=org,
                                                        applicant=user_info,
                                                        application_status=0)
    if 0 < len(applications):
        result['notice'] = 'You already have another pending application for this club.'
        return result
        
    result['success'] = True
    new_application = MembershipApplication.objects.create(organization=org, applicant=user_info,
                                                           application_status=0,
                                                           apply_time=datetime.datetime.now())
    new_application.save()
    
    return result
# Ending of function join_org(cookie_id, org_id)


# creator不能退出社团
def exit_org(cookie_id, org_name):  # 退出社团
    response = Person.objects.filter(cookie_id=cookie_id)
    result = {}
    result['success'] = False
    if len(response) == 0:
        result['notice'] = 'The cookie_id does not exist.'
        return result
    elif expire(response[0].cookie_expire):
        result['notice'] = 'The cookie_id is out of date.'
        return result
    
    response_1 = Organizations.objects.filter(organization_name=org_name)  # 获取该社团信息
    user_info = response[0].user_info
    if len(response_1) == 0:  # 该社团不存在
        result['notice'] = 'The organization does not exist.'
        return result
    org = response_1[0]
    
    members = org.members.all()
    if user_info not in list(members):
        result['notice'] = 'You are not in this club.'
        return result
    
    if user_info == org.master:
        result['notice'] = 'Club manager cannot quit the club.'
        return result
    
    org.members.remove(user_info)
    org.save()
    
    result['success'] = True
    now_time = datetime.datetime.now()
    new_application = MembershipApplication.objects.create(organization=org,
                                                           applicant=user_info,
                                                           application_status=3,
                                                           apply_time=now_time,
                                                           solve_time=now_time)
    new_application.save()
    
    return result
# Ending of function exit_org(cookie_id, org_name)


# 社团管理员发布社团活动信息
def publish_activ(cookie_id, info):
    response = Person.objects.filter(cookie_id=cookie_id)
    result = {}
    result['success'] = False
    if len(response) == 0:
        result['notice'] = 'The cookie_id is not exist.'
        return result
    elif expire(response[0].cookie_expire):
        result['notice'] = 'The cookie_id is out of date.'
        return result
    
    activ_duplicate = info['org'].activ_organization.filter(activ_name=info['activ_name'])
    if 0 < len(activ_duplicate):
        result['notice'] = 'Duplicate activity name: "' + info['activ_name'] + '".'
        return result
    
    try:
        activ_time = datetime.datetime.strptime(info['activ_time'], '%Y-%m-%d')
    except ValueError:
        activ_time = None
    
    activ = Activ.objects.create(activ_name=info['activ_name'],
                                 activ_time=activ_time,
                                 organization=info['org'],
                                 activ_place=info['activ_place'],
                                 activ_content=info['activ_content'])
    activ.save()
    result['success'] = True
    return result


# 社团成员、管理员查看社团活动信息
def look_org_activ(cookie_id, org_name):
    response = Person.objects.filter(cookie_id=cookie_id)
    result = {}
    result['success'] = False
    if len(response) == 0:
        result['notice'] = 'Not Logged.'
        return result
    elif expire(response[0].cookie_expire):
        result['notice'] = 'Not Logged.'
        return result
    
    org_info = Organizations.objects.filter(organization_name=org_name, create_status=1)
    if len(org_info) == 0:
        result['notice'] = 'The organization does not exist.'
        return result
    
    activ_info = Activ.objects.filter(organization=org_info[0]).order_by('-activ_time')
    activ_list = []
    for each in activ_info:
        activ_time = ''
        if each.activ_time is not None:
            activ_time = each.activ_time.strftime("%Y-%m-%d")
        activ_list.append({'org_name': each.organization.organization_name,
                           'activ_name': each.activ_name,
                           'activ_time': activ_time,
                           'activ_place': each.activ_place,
                           'activ_content': each.activ_content})
    result['activ_list'] = activ_list
    result['success'] = True
    return  result
# Ending of function look_org_activ(cookie_id, org_name)
