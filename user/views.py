from user.form import NewUser, LoginUser, EditUser, NewPass, DeleteUser
from django.http import HttpResponseRedirect, Http404
from django.template.context_processors import csrf
from soyzniki.main.auth import is_login, user_id
from user.models import User, Secret
from django.shortcuts import render
from django.contrib import messages
from soyzniki.main.auth import hash_user_pass
# from threading import Thread
# from soyzniki.main.send_email import send_email


def user_page(request, login):
    if is_login(request):
        user = User.objects.get(id=user_id(request))
        user_page = User.objects.get(login=login)
        if user == user_page:
            data = {
                'login': True,
                'view': True,
                'user': user,
                'user_page': user_page,
                'account_class': 'active',
            }
            data.update(csrf(request))
        else:
            data = {
                'login': True,
                'view': False,
                'user': user,
                'user_page': user_page,
                'account_class': 'active',
            }
            data.update(csrf(request))
        return render(request, 'user_page.html', data)
    else:
        return HttpResponseRedirect('/user/login/')


def login(request):
    if not is_login(request):
        if request.method == 'POST':
            form = LoginUser(request.POST)
            if form.is_valid():
                fields = form.clean()
                if fields.get('saved'):
                    request.session['user'] = fields.get('shadow_id')
                    return HttpResponseRedirect('/user/{}/'.format(fields.get('user')))
                else:
                    response = HttpResponseRedirect('/user/{}/'.format(fields.get('user')))
                    response.set_cookie('xsstoken', fields.get('shadow_id'))
                    return response
            else:
                data = {
                    'form': form,
                    'account_class': 'active',
                    'login': False
                }
            data.update(csrf(request))
            return render(request, 'user_login.html', data)
        else:
            form = LoginUser()
            data = {
                'form': form,
                'account_class': 'active',
                'login': False
            }
            data.update(csrf(request))
            return render(request, 'user_login.html', data)
    else:
        user = User.objects.get(id=user_id(request))
        return HttpResponseRedirect('/user/{}/'.format(user.login))


def add(request):
    if not is_login(request):
        if request.method == 'POST':
            form = NewUser(request.POST)
            if form.is_valid():
                form.save()
                messages.info(request, 'Вы успешно зареристриваны.')
                messages.info(request, 'Проверьте почту указанную при регистрации.')
                return HttpResponseRedirect('/')
            else:
                data = {
                    'form': form,
                    'account_class': 'active',
                    'login': False
                }
                data.update(csrf(request))
                return render(request, 'user_add.html', data)
        else:
            form = NewUser()
            data = {
                'form': form,
                'account_class': 'active',
                'login': False
            }
            data.update(csrf(request))
            return render(request, 'user_add.html', data)
    else:
        return HttpResponseRedirect('/user/login/')


def activate(request, login, data):
    if is_login(request):
        raise Http404
    else:
        user = User.objects.get(login=login)
        if user.activate:
            raise Http404
        else:
            secret = Secret.objects.get(user_id=user.id)
            key = hash_user_pass(
                str(secret.sol),
                str(secret.shadow_id)
            )
            if key == data:
                user.activate = True
                user.save()
                messages.info(request, 'Ваша учетная запись активирована')
                request.session['user'] = secret.shadow_id
                return HttpResponseRedirect('/user/{}/'.format(
                    user.login
                ))
            else:
                messages.info(request, 'Ошибка, Обратитесь к администрации сайта')
                return HttpResponseRedirect('/')


def logout(request):
    if is_login(request):
        sess = False
        cook = False
        try:
            secret = Secret.objects.get(id=user_id(request))
        except Secret.DoesNotExcist:
            raise Http404
        else:
            try:
                user = request.session['user']
            except KeyError:
                try:
                    user = request.COOKIES['xsstoken']
                except KeyError:
                    raise Http404
                else:
                    cook = True
            else:
                sess = True
        if secret.shadow_id == user:
            response = HttpResponseRedirect('/')
            if sess:
                del request.session['user']
            if cook:
                response.delete_cookie('xsstoken')
        return response
    else:
        return HttpResponseRedirect('/user/login/')


def edit(request, login):
    if is_login(request):
        user = User.objects.get(id=user_id(request))
        if user.login != login:
            raise Http404
        if request.method == 'POST':
            form = EditUser(request.POST)
            print(request.POST)
            if form.is_valid():
                form.save(user_id(request))
                messages.info(request, 'Ваши данные успешно изменены')
                return HttpResponseRedirect('/user/{}/'.format(user.login))
            else:
                data = {
                    'user': user,
                    'account_class': 'active',
                    'form': form,
                    'login': True
                }
                data.update(csrf(request))
                return render(request, 'user_edit.html', data)
        else:
            user_data = {
                'name': user.name,
                'family': user.family,
                'email': user.email,
                'telephone': user.telephone,
                'country': user.country.name_ru,
                'region': user.region.name_ru,
                'district': user.district.name_ru,
                'city': user.city.name_ru,
                'street': user.street,
                'country_id': user.country.id,
                'region_id': user.region.id,
                'district_id': user.district.id,
                'city_id': user.city.id,
            }
            form = EditUser(initial=user_data)
            data = {
                'user': user,
                'account_class': 'active',
                'form': form,
                'login': True
            }
            data.update(csrf(request))
            return render(request, 'user_edit.html', data)
    else:
        return HttpResponseRedirect('/user/login/')


def edit_pass(request, login):
    if is_login(request):
        user = User.objects.get(id=user_id(request))
        if user.login != login:
            raise Http404
        if request.method == 'POST':
            form = NewPass(request.POST)
            print(request.POST)
            if form.is_valid():
                form.save(user_id(request))
                messages.info(request, 'Ваш пароль успешно изменен')
                return HttpResponseRedirect('/user/{}/'.format(user.login))
            else:
                data = {
                    'form': form,
                    'account_class': 'active',
                    'user': user,
                    'login': True,
                }
                data.update(csrf(request))
                return render(request, 'user_edit_pass.html', data)
        else:
            user_data = {
                'user_login': user.login,
            }
            form = NewPass(initial=user_data)
            data = {
                'form': form,
                'account_class': 'active',
                'user': user,
                'login': True,
            }
            data.update(csrf(request))
            return render(request, 'user_edit_pass.html', data)
    else:
        return HttpResponseRedirect('/user/login/')


def delete(request, login):
    if is_login(request):
        user = User.objects.get(id=user_id(request))
        if user.login != login:
            raise Http404
        if request.method == 'POST':
            form = DeleteUser(request.POST)
            if form.is_valid():
                User.objects.filter(id=user_id(request)).delete()
                response = HttpResponseRedirect('/')
                try:
                    del request.session['user']
                except KeyError:
                    response.delete_cookie('xsstoken')
                return response
            else:
                data = {
                    'user': user,
                    'account_class': 'active',
                    'form': form,
                    'login': True,
                }
                data.update(csrf(request))
                return render(request, 'user_delete.html', data)
        else:
            user_data = {
                'user_login': user.login,
            }
            form = DeleteUser(initial=user_data)
            data = {
                'user': user,
                'account_class': 'active',
                'form': form,
                'login': True,
            }
            data.update(csrf(request))
            messages.info(request, 'Ваша станица будет удалена без возможности востановления')
            return render(request, 'user_delete.html', data)
    else:
        return HttpResponseRedirect('/user/login/')
