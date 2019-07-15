from .database import function
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from . import view,view_special
from people.models import Organizations, ClubPronounces


# def user_in_club


def clubbulletin(request):
	context = {}
	cookie_id = request.COOKIES.get('id', None)
	result = function.get_user_info(cookie_id)
	if not result['success']:
		return view.response_not_logged_in(request)
	
	org_name = request.GET.get('iden', None)
	org = Organizations.objects.filter(organization_name=org_name)
	if 0 == len(org):
		return HttpResponseRedirect('../index/')
	
	info = result['info']
	context['islogin'] = True
	context['name'] = info['user_name']
	context['org_name'] = org_name
	context['pronounces'] = org.pronounces.all()
	
	return HttpResponse(render(request, 'clubbulletin.html', context))


def addpronounce(request):
	''


