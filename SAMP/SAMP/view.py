from django.shortcuts import render
from django.http import *
from .Cookie import *
from .check_valid import *
from .verify import *
from .database.delete import *
from .database.save import *
from .database.search import *
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
        if not pswd_correct(username, pswd):
            context['login_fail_notice'] = 'Wrong Username or Password!'
            return HttpResponse(render(request, 'login.html', context))
        context['title'] = 'Login Success'
        context['url'] = '../index/'
        context['error_msg'] = 'You have logged in successfully!'
        response = HttpResponse(render(request, 'jump.html', context))
        cookie = Cookie()
        save_cookie(user_of_username(username),cookie)
        response.set_cookie('id', cookie.cookie_id, expires=cookie.expire)
        return response
    else:
        response=HttpResponse(render(request, 'login.html'))
        response.delete_cookie('id')
        return response


def logout(request):
    context={}
    context['title'] = 'Logout Success'
    context['url'] = '../index/'
    context['error_msg'] = 'You have logged out successfully!'
    response = HttpResponse(render(request, 'jump.html', context))
    response.delete_cookie('id')
    cookie_id = request.COOKIES.get('id',None)
    if cookie_id is not None:
        delete_cookie(cookie_id)
    return response


def index(request):
    context = {}
    user=None
    if request.COOKIES.get('id') is not None:
        user = user_of_cookie(request.COOKIES.get('id'))

    response = HttpResponse()
    if user is not None:
        context['name'] = user.name
        cookie = Cookie()
        save_cookie(user, cookie)
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
            save_name_pswd(username, password1)
            context['title']='Register Success'
            context['url']='../login/'
            context['error_msg'] = 'You have registered successfully!'
            return HttpResponse(render(request, 'jump.html', context))
        else:
            context['register_fail_notice'] = verify_result
        return HttpResponse(render(request, 'register.html', context))
    else:
        return HttpResponse(render(request, 'register.html'))


def response_not_logged_in(request):
    context = {}
    context['title'] = 'Not logged in'
    context['url'] = '../login/'
    context['error_msg'] = 'You are not logged, please log in!'
    response = HttpResponse(render(request, 'jump.html', context))
    return response
