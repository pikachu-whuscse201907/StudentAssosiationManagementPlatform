from django.shortcuts import render
from django.http import *


def page_not_found(request,exception):
    context={}
    context['notice']=''
    response=HttpResponse(render(request, '404.html',context))
    return response


def page_internal_error(request,exception):
    context = {}
    context['notice'] = ''
    response = HttpResponse(render(request, '500.html', context))
    return response