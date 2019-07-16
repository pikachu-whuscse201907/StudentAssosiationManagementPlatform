from people.models import Organizations
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .database import function
from . import view
from .database import search


class clubclass:
    def __init__(self, _org_name, _descript):
        self.org_name = _org_name
        self.descript = _descript


def searchclub(request):
    request.encoding='utf-8'
    dic = {}
    cookie_id = request.COOKIES.get('id', None)
    if cookie_id is not None:
        result = function.get_user_info(cookie_id)  # call database
        if result['success']:
            info = result['info']
            dic['islogin'] = True
            dic['name'] = info['user_name']
    
    if "search_context" in request.GET:
        keyword = request.GET["search_context"]
        if keyword == "":
            return render(request, "searchclub.html", {"error": "you should input something!"})
        else:
            infodic = function.search_org(request.COOKIES["id"], keyword)
            if infodic["success"] == False:
                return render(request, "searchclub.html", {"error": infodic["notice"]})
            clublist = infodic["org_list"]
            clubs = []
            if len(clublist) == 0:
                return render(request, "searchclub.html", {"error": "no result!"})
            for each in clublist:
                club = clubclass(each[0], each[1])  # org_name and description
                clubs.append(club)
            dic["clubs"] = clubs
            return render(request, "searchclub.html", dic)
    return render(request, "searchclub.html")


def clubinfo(request):
    context = {}
    cookie_id = request.COOKIES.get('id', None)
    if cookie_id is not None:
        result = function.get_user_info(cookie_id)  # call database
        if result['success']:
            info = result['info']
            context['islogin'] = True
            context['name'] = info['user_name']
    
    if "iden" in request.GET:
        org_name = request.GET["iden"]
        result = search.get_org_info(org_name, cookie_id)
        
        if result["success"] == False:
            context["error"] = result["notice"]
            return render(request, "clubpage.html", context)
        
        org_info = result["org_info"]
        
        context["org_logo"] = org_info["org_logo"]
        context["org_name"] = org_info['org_name']
        context["org_description"] = org_info['org_description']
        if org_info['create_date'] is None:
            context['create_date'] = 'Not Recorded'
        else:
            context['create_date'] = org_info['create_date'].strftime('%Y-%m-%d')
        context["org_master"] = org_info['org_master']
        context["creator"] = org_info['creator']
        context["member_num"] = org_info['member_num']
        context["isjoin"] = org_info['isjoin']
        
        return render(request, "clubpage.html", context)
    
    return HttpResponseRedirect("../searchclub/")


def joinclub(request):
    context = {}
    cookie_id = request.COOKIES.get('id', None)
    user = search.user_of_cookie(cookie_id)
    user_info = search.user_info_of_user(user)
    
    if user_info is None:
        return view.response_not_logged_in(request)
    context['islogin'] = True
    
    org_name = request.GET.get('iden', None)
    if org_name is None:
        return render(request, "searchclub.html")
    
    result = function.join_org(cookie_id, org_name)
    
    if result["success"] == False:
        result = search.get_org_info(org_name, cookie_id)

        org_info = result["org_info"]
        context["org_logo"] = org_info["org_logo"]
        context["org_name"] = org_info['org_name']
        context["org_description"] = org_info['org_description']
        if org_info['create_date'] is None:
            context['create_date'] = 'Not Recorded'
        else:
            context['create_date'] = org_info['create_date'].strftime('%Y-%m-%d')
        context["creator"] = org_info['creator']
        context["member_num"] = org_info['member_num']
        context["isjoin"] = org_info['isjoin']
        
        context["error"] = result["notice"]
        return render(request, "clubpage.html", context)
    
    else:  # function.join_org returned True
        return render(request, "jump.html",
                      {"title": "Applied to join successfully!",
                       "url": ("../clubinfo/?iden={0}".format(org_name)),
                       "error_msg": "You have applied to join successfully!"})


def quitclub(request):
    context = {}
    cookie_id = request.COOKIES.get('id', None)
    user = search.user_of_cookie(cookie_id)
    user_info = search.user_info_of_user(user)
    
    if user_info is None:
        return view.response_not_logged_in(request)
    
    iden = request.GET.get('iden', None)
    if iden is None:
        return render(request, "jump.html", {"title": "error!", "url": "/", "error_msg": "You have failed quiting the association!"})
    
    result1 = function.exit_org(cookie_id, iden)
    if result1["success"] == False:
        context = {}
        context['islogin'] = True
        org_name = request.GET["iden"]
        result = search.get_org_info(org_name, request.COOKIES['id'])
        if result["success"] == False:
            context["error"] = result["notice"]
            return render(request, "clubpage.html", context)
        org_info = result["org_info"]
        context["org_logo"] = org_info["org_logo"]
        context["org_name"] = org_info['org_name']
        context["org_description"] = org_info['org_description']
        if org_info['create_date'] is None:
            context['create_date'] = 'Not Recorded'
        else:
            context['create_date'] = org_info['create_date'].strftime('%Y-%m-%d')
        context["creator"] = org_info['creator']
        context["member_num"] = org_info['member_num']
        context["error"] = result1["notice"]
        context["isjoin"] = org_info['isjoin']
        return render(request, "clubpage.html", context)
    return render(request, "jump.html", {"title": "quit successfully!", "url": "../", "error_msg": "You have quited the association successfully!"})


