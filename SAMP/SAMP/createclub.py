from django.shortcuts import render
from . import verify, imgop
from .database import function

def createclub(request):
       if request.method == "POST":
              name = request.POST["creater"]
              des = request.POST["org_description"]
              iden = request.POST["org_name"]
              image = request.FILES["org_photo"]
              check = verify.verifyclub(name, des, iden)
              if check != True:
                     return render(request, "createclub.html", {"error": check})
              result = function.create_org(request.COOKIES["id"], name, iden, des, image)
              if result["success"] == False:
                     return render(request, "createclub.html", {"error": result["notice"]})
              else:
                     return render(request, "jump.html", {"error_msg": "Successfully", "url": "../index/", "title": "Create successfullly"})
       return render(request, "createclub.html")
