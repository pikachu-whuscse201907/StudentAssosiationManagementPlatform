from people.models import Organizations
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .database import function
from . import imgop,view
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
		result = search.get_org_info(org_name)

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
	
		return render(request, "clubpage.html", context)
	
	return HttpResponseRedirect("../searchclub/")

