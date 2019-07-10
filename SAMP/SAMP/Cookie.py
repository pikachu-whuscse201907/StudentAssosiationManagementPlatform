import time
import datetime
import random
from people.models import Person
COOKIE_AGE_HOURS=3


class Cookie:
    def __init__(self):
        self.cookie_id = random.sample('0123456789abcdef',128)
        self.create_time = datetime.datetime()
        self.expire = datetime.timedelta(hours=COOKIE_AGE_HOURS)


def get_user_from_cookie(_cookie_id):
    p=Person.objects.filter(cookie_id=_cookie_id)
    if len(p) == 0:
        # No such cookie in database.
        return None

    now = datetime.datetime()
    if p[0].cookie_expire > now or p[0].cookie_expire is None:
        p[0].cookie_id = ''
        p[0].cookie_create_time = None
        p[0].cookie_expire = None
    return p[0]


def get_user_from_username_pswd(_username,_pswd):
    p = Person.objects.filter(username=_username,pswd=_pswd)
    if len(p) == 0:
        # No such user in database.
        return None
    return p[0]


def write_cookie(user, cookie):
    user.cookie_id = cookie.cookie_id
    user.cookie_create_time = cookie.create_time
    user.cookie_expire = cookie.expire
    user.save()
