from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from . import view
from .database import function, search, delete


def passwd(request):
    context = {}
    cookie_id = request.COOKIES.get('id', None)
    result = function.get_user_info(cookie_id)
    if not result['success']:
        return view.response_not_logged_in(request)

    info = result['info']
    context['name'] = info['user_name']
    context['user_logo'] = info['user_logo']
    
    name = request.POST.get('name', None)
    rawpsd = request.POST.get('rawpsd', None)
    newpsd = request.POST.get('newpsd', None)
    cnewpsd = request.POST.get('cnewpsd', None)

    if name is None or rawpsd is None or newpsd is None or cnewpsd is None:
        return HttpResponse(render(request, 'passwd.html', context))

    if name is not None and not search.pswd_correct(name, rawpsd):
        delete.delete_cookie(cookie_id)
    else:
        if info['user_name'] == name and newpsd == cnewpsd:
            user = search.user_of_username(name)
            user.pswd = newpsd
            user.save()
            context['title'] = '修改密码成功'
            context['url'] = '../userpage/'
            context['error_msg'] = '修改密码成功'
            return HttpResponse(render(request, 'jump.html', context))

    return HttpResponse(render(request, 'passwd.html', context))


def checkpsd(request):
    cookie_id = request.COOKIES.get('id', None)
    result = function.get_user_info(cookie_id)
    if not result['success']:
        return HttpResponse("False")
    info = result['info']
    name = request.POST.get('name', None)
    pswd = request.POST.get('pwsd', None)
    if name is not None and pswd is not None:
        if info['user_name'] == name and search.pswd_correct(name, pswd):
            return HttpResponse("True")
    
    return HttpResponse("False")
