# -*- coding: utf-8 -*-
from people.models import Person, User_info, Organizations
from ..Cookie import expire


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
    if username is None or password is None:
        return False
    user = user_of_username(username)
    if user is None:
        return False
    
    if user.pswd == password:
        return True   # 密码相同
    return False


def user_of_username(username):
    if username is None:
        return None
    p = Person.objects.filter(name=str(username))
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


def get_org_info(org_name, cookie_id):
    result = {}
    result['success'] = False
    org_info = {}  # result字典中key 'org_info'对应的value
    response_1 = Organizations.objects.filter(organization_name=org_name)
    
    if 0 == len(response_1):
        result['notice'] = 'No such organization.'
        result['org_info'] = org_info
        return result

    response = Person.objects.filter(cookie_id=cookie_id)
    user_info = User_info.objects.filter(name=response[0])
    c = response_1[0].members.all()
    if user_info[0] in c:
        org_info['isjoin'] = True
    else:
        org_info["isjoin"] = False
        if 1 != response_1[0].create_status:
            result['notice'] = 'No such organization.'
            result['org_info'] = org_info
            return result
    
    org_info['org_name'] = response_1[0].organization_name
    org_info['org_description'] = response_1[0].description
    org_info["org_status"] = response_1[0].create_status
    org_info['create_date'] = response_1[0].create_date
    org_info['org_master'] = response_1[0].master.name.name
    org_info['creator'] = response_1[0].creator.name.name
    org_info['member_num'] = len(response_1[0].members.all())
    org_info['org_logo'] = response_1[0].org_logo
    
    result['org_info'] = org_info
    result['success'] = True
    return result
# Ending of function get_org_info(org_name, cookie_id).
