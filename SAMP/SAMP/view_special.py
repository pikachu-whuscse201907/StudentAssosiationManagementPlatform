from django.shortcuts import render
from django.http import *


def page_not_found(request, exception):
    context={}
    context['title'] = '404 Not Found'
    context['url'] = '../index/'
    context['error_msg']='Request Page Not Found'
    response = HttpResponse(render(request, 'jump.html', context))
    return response


def page_internal_error(request, exception):
    context = {}
    context['title'] = '500 Internal Error'
    context['url'] = '../index/'
    context['error_msg'] = 'Internal Server Error'
    response = HttpResponse(render(request, 'jump.html', context))
    return response