import time
import datetime
import pytz
import random
from people.models import Person

COOKIE_AGE_HOURS = 3


class Cookie:
    def __init__(self):
        self.cookie_id = gen_rand_hex(128)
        # print("id:", self.cookie_id)
        self.create_time = datetime.datetime.now()
        self.expire = (datetime.datetime.now()+datetime.timedelta(hours=COOKIE_AGE_HOURS))


def gen_rand_hex(len):
    ans = ''
    for i in range(len):
        ans+=(random.choice('0123456789abcdef'))
    return ans


def expire(cookie_expire):
    if cookie_expire is None:
        return True
    now = datetime.datetime.now()
    now = now.replace(tzinfo=pytz.timezone('UTC'))
    delta = now - cookie_expire
    if delta > datetime.timedelta(seconds=1):
        return True
    else:
        return False


