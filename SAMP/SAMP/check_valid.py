def valid_username_pswds(username,password1,password2):
    if len(username)<5:
        return False
    if len(password1)<8 or len(password1)>30:
        return False
    if password1 != password2:
        return False
    if contain_bad_char(username):
        return False
    return True


def contain_bad_char(username):
    return False
