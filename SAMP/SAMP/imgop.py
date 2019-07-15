from people.models import  Organizations, Person

def update_org_logo(cookie_id, img, iden):
       imgiden = "img_" + iden
       result = {}
       try:
              org = Organizations.objects.get(number = iden)
       except:
              result["success"] = False
              result["notice"] = "no such association"
              return result
       try:
              people = Person.objects.get(cookie_id = cookie_id)
       except:
              result["success"] = False
              result["notice"] = "You haven't log in!"
              return result
       if not org.img:
              image = Orgimage(img = img, name = imgiden)
              image.save()
              org.img = image
              org.save()
       else:
              org.img.img = img
              org.img.name = imgdien
              org.img.save()
              org.save()
       result["success"] = True
       return result


def get_org_logo(cookie_id, org_id):
       result = {}
       try:
              org = Organizations.objects.get(number = org_id)
       except:
              result["success"] = False
              result["notice"] = "You haven\'t log in the association!"
              return result
       result["success"] = True
       result["org_logo"] = org.img.img
       return result
