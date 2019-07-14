from people.models import Organizations
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .database import function
from . import imgop
from .database import save

class clubclass:
       def __init__(self, iden, info):
              self.iden = iden
              self.info = info

def searchclub(request):
       request.encoding='utf-8'
       dic = {}
       dic["islogin"] = True
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
                            club = clubclass(each[0], each[1])
                            clubs.append(club)
                     dic["clubs"] = clubs
                     return render(request, "searchclub.html", dic)
       return render(request, "searchclub.html")

def clubinfo(request):
       if "iden" in request.GET:
              clubid = request.GET["iden"]
              dic = {}
              dic["islogin"] = True
              result = save.get_org_info(request.COOKIES["id"], clubid)
              imgresult = imgop.get_org_logo(request.COOKIES["id"], clubid)
              if result["success"] == False:
                     dic["error"] = result["notice"]
                     return render(request, "clubinfo.html", dic)
              if imgresult["success"] == False:
                     dic["error"] = imgresult["notice"]
                     return render(request, "clubinfo.html", dic)
              dic = result["org_info"]
              dic["islogin"] = True
              dic["image"] = imgresult["org_logo"]
              return render(request, "clubpage.html", dic)















              
