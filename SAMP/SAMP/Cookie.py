import time
import datetime
import pytz
import random
from people.models import Person

COOKIE_AGE_HOURS = 3


class Cookie:
    def __init__(self):
        self.cookie_id = gen_rand_hex(128)
        self.create_time = datetime.datetime.now()
        self.expire = (datetime.datetime.now()+datetime.timedelta(hours=COOKIE_AGE_HOURS))


def gen_rand_hex(len):
    ans = ''
    for i in range(len):
        ans.join(random.choice('0123456789abcdef'))
    return ans

def get_user_from_cookie(_cookie_id):
    p=Person.objects.filter(cookie_id=_cookie_id)
    if len(p) == 0:
        # No such cookie in database.
        return None

    now = datetime.datetime.now()
    delta = None
    if p[0].cookie_expire is not None:

        now=now.replace(tzinfo=pytz.timezone('UTC'))
        print(now.tzinfo)
        print(p[0].cookie_expire.tzinfo)
        delta = now - p[0].cookie_expire
    if delta is None or delta > datetime.timedelta(seconds=1):
        p[0].cookie_id = ''
        p[0].cookie_create_time = None
        p[0].cookie_expire = None
    return p[0]


def get_user_from_username_pswd(_username,_pswd):
    p = Person.objects.filter(name=_username,pswd=_pswd)
    if len(p) == 0:
        # No such user in database.
        return None
    return p[0]


def write_cookie(user, cookie):
    user.cookie_id = cookie.cookie_id
    user.cookie_create_time = cookie.create_time
    user.cookie_expire = cookie.expire
    user.save()

def new_user(_username,_password):
    p=Person.objects.create(name=_username,pswd=_password)
    p.save()