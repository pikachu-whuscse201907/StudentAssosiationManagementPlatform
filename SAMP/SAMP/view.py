from django.shortcuts import render
from django.http import *
from .Cookie import *
import time


def login(request):
    context = {}
    user = None
    if request.POST.get('username') is not None and request.POST.get('pswd') is not None:
        user = get_user_from_username_pswd(request.POST.get('id'),request.POST.get('pswd'))
    if user is None:
        context['login_fail_notice'] = 'Wrong Username or Password!'
        return HttpResponse(render(request, 'login.html', context))

    response = HttpResponseRedirect('index/')
    cookie = Cookie()
    response.set_cookie('id', cookie.id, cookie.expire)
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
        response.set_cookie('id', cookie.id, cookie.expire)

    response.content = render(request, 'index.html', context)

    return response


def register(request):
    ''
