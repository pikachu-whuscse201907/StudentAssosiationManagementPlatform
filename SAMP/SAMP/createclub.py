from django.shortcuts import render
from . import verify
from .database import function,search
from . import view
from django.http import HttpResponse,HttpResponseRedirect


def createclub(request):
	context = {}
	cookie_id = request.COOKIES.get('id', None)
	if cookie_id is None:
		return view.response_not_logged_in(request)
	
	result = function.get_user_info(cookie_id)  # call database
	if not result['success']:
		return view.response_not_logged_in(request)
	info = result['info']
	
	context['islogin'] = True
	context['name'] = info['user_name']
	
	creator_name = info['user_name']
	des = request.POST.get("org_description", None)
	iden = request.POST.get("org_name", None)
	image = request.FILES.get("org_photo", None)
	
	if creator_name is None or des is None or iden is None or image is None:
		response = HttpResponse(render(request, 'createclub.html', context))
		return response
	
	check = verify.verifyclub(creator_name, des, iden)
	if check != True:
		context['createclub_fail_notice'] = check
		return render(request, "createclub.html",context)
	result = function.create_org(cookie_id, creator_name, iden, des, image)
	if result["success"] == False:
		context['error'] = result["notice"]
		return render(request, "createclub.html", context)
	else:
		context['title'] = 'Create Organization Success'
		context['url'] = '../clubpage/?iden=' + iden
		context['error_msg'] = 'You have created an organization successfully!'
		return render(request, "jump.html", context)

