# -*- coding: utf-8 -*-
from django.http import HttpResponse
from .view import *

#注册函数
def db_register():
    response = Person.objects.select_related("pswd").filter(name=username)

    if response == None:   #用户名未创建
        if password1 == password2:
            password = password1
            test1 = Person(name=username, pswd=password)
            test1.save()
            return 'register successfully'    #点击确认按钮后跳转至用户页面
        else:
            return 'the passwords are not the same'   #密码不一致！请重新输入！
    else:
        return 'this username has existed'   #用户名已建立，需修改用户名

#登录函数
def db_login():
    Person.objects.order_by("name")
    response = Person.objects.select_related("pswd").filter(name=username)

    if response == None:
        return 'no existing username'           #提示：用户名不存在
    else:
        if password == response:
            return 'login successfully'       #登陆成功，页面跳转
        else:
            return 'password is wrong'       #提示：密码输入错误

