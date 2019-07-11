from django.shortcuts import render
from django.http import *
from .Cookie import *
from .check_valid import *
from .verify import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import *
import time


def redir_to_index(request):
    return HttpResponseRedirect('index/')


def login(request):
    context = {}
    username=request.POST.get('username', None)
    pswd=request.POST.get('pswd', None)
    if username is not None and pswd is not None:
        user = get_user_from_username_pswd(username, pswd)
        if user is None:
            context['login_fail_notice'] = 'Wrong Username or Password!'
            return HttpResponse(render(request, 'login.html', context))

        response = HttpResponseRedirect('../index/')

        cookie = Cookie()
        response.set_cookie('id', cookie.cookie_id, expires=cookie.expire)
        return response
    else:
        response=HttpResponse(render(request, 'login.html'))
        response.delete_cookie('id')
        return response


def logout(request):
    context={}
    response = HttpResponseRedirect('../index/')
    if request.COOKIES.get('id') is not None:
        user = get_user_from_cookie(request.COOKIES.get('id'))
        #delete cookie from database
        response.delete_cookie('id')
    return response


def index(request):

    context = {}
    user=None
    if request.COOKIES.get('id') is not None:
        user = get_user_from_cookie(request.COOKIES.get('id'))

    response = HttpResponse()
    if user is not None:
        context['name'] = user.name
        cookie = Cookie()
        write_cookie(user, cookie)
        response.set_cookie('id', cookie.cookie_id, expires=cookie.expire)

    response.content = render(request, 'index.html', context)

    return response


def register(request):
    context = {}
    username = request.POST.get('username', None)
    password1 = request.POST.get('password1', None)
    password2 = request.POST.get('password2', None)
    if username is not None and password1 is not None and password2 is not None:
        verify_result = veri(username, password1, password2)
        if veri(username, password1, password2) == True:
            #write info into database
            return HttpResponseRedirect('../login/')
        else:
            context['register_fail_notice'] = verify_result
        return HttpResponse(render(request, 'register.html', context))
    else:
        return HttpResponse(render(request, 'register.html'))


def creatclub(request):
    context={}
    response=HttpResponse(render(request, 'creatclub.html'))
    return response


def searchclub(request):
    context={}
    response=HttpResponse(render(request, 'searchclub.html'))
    return response


def userpage(request):
    context={}
    response=HttpResponse(render(request, 'userpage.html'))
    return response



