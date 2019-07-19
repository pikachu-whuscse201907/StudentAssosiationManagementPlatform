from people.models import Person
from .database import search


def veri(username, password, conpass):
    "verify the validity"
    if password != conpass:
        return "please check your password and confirmed password!"
    elif len(username) < 4:
        return "your username is too short. The username must be more than 4 chars!"
    elif len(str(password)) < 6:
        return "your password is too short. The password must be more than 6 chars!"
    else:
        for each in username:
            if is_uchar(each):
                continue
            else:
                return "Your username includes invalid char!"
    if search.user_existing(username):
        return "The username has been registered!"
    return True


def verifyclub(name, des, iden):
    if name == "":
        return "You should input your name!"
    elif des == "":
        return "You should input your club's description!"
    elif iden == "":
        return "You should input your club's name!"
    else:
        for each in iden:
            if is_uchar(each):
                continue
            else:
                return "Your username includes invalid char!"
        return True


def is_uchar(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
        """判断一个unicode是否是数字"""
    elif uchar >= u'\u0030' and uchar <= u'\u0039':
        return True
        """判断一个unicode是否是英文字母"""
    elif (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
        return True
    elif uchar == u'\u005f':
        return True
    return False