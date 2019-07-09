import time
from people.models import Person


def get_user_from_cookie(_cookie_id):
    p=Person.objects.filter(cookie_id=_cookie_id)
    if len(p)==0:
        return None
    return p[0].name


def new_cookie():
    return time.time()


def write_cookie(username,_cookie_id):
    p=Person.objects.filter(name=username)

    if len(p) == 0:
        p=Person.objects.create(name=username, cookie_id=_cookie_id)
    else:
        p[0].cookie_id=_cookie_id
        p[0].save()