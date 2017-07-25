from hashlib import md5
from random import randint


def hash_user_pass(user_pass, sol):
    h_pass = md5()
    h_pass.update(user_pass.encode('utf-8') + sol.encode('utf-8'))
    return h_pass.hexdigest()


def rand_long_int():
        return str(randint(1000000000000000, 9999999999999999999))


def is_login(request):
    from user.models import User, Secret
    try:
        shadow_id = request.session['user']
    except KeyError:
        try:
            shadow_id = request.COOKIES['xsstoken']
        except KeyError:
            return False
    user = Secret.objects.get(shadow_id=shadow_id)
    try:
        User.objects.get(id=user.id)
    except User.DoesNotExcist:
        return False
    else:
        return True


def user_id(request):
    from user.models import Secret
    if is_login(request):
        try:
            shadow_id = request.session['user']
        except KeyError:
            shadow_id = request.COOKIES['xsstoken']
        user = Secret.objects.get(shadow_id=shadow_id)
        return user.id
    else:
        raise Exception
