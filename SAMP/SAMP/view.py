from django.shortcuts import render
from django.http import HttpResponse
from .Cookie import *
import time

def login(request):
    ''
    # POST: username+pswd
    # response 302
    # if success: to index(logged)
    # if fail: to login, failure notice


def index(request):


    context = {}
    username=''
    if request.COOKIES.get('id') is not None:
        username_cookie=get_user_from_cookie(request.COOKIES.get('id'))
        username = username_cookie

    if request.GET.get('user') is not None:
        username_get=request.GET.get('user')
        username = username_get

    print(username)
    if username is not None:
        context['helloname'] = username

    response=HttpResponse(render(request, 'index.html', context))
    cookie=new_cookie()
    response.set_cookie('id',cookie,3600)
    if username is not None:
        write_cookie(username,cookie)
    return response
