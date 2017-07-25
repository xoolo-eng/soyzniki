from django.shortcuts import render
from django.template.context_processors import csrf
from soyzniki.main.auth import is_login, user_id
from django.http import Http404, HttpResponseRedirect
from django.contrib import messages
from partner.forms import FormPatrner, LoginSearch, DataSearch
from partner.forms import FormPatrnerEdit, DelPartner, AddPoint
from user.models import User
from partner.models import Partner, Point
from soyzniki.main.pages import count_page, get_html_pages
from django.core.cache import cache


COUNT_ELEMENTS = 20


def all(request):
    '''
    вывод всех партнерских страниц пользователя
    '''
    user = User.objects.get(id=user_id(request))
    partners = user.users.filter(active=True)
    data = {
        'login': True,
        'user': user,
        'account_class': 'active',
        'partners': partners,
    }
    data.update(csrf(request))
    return render(request, 'partner_all.html', data)


def add(request):
    '''
    создание новой страницы партнера
    '''
    if is_login(request):
        user = User.objects.get(id=user_id(request))
        if request.method == 'POST':
            form_partner = FormPatrner(request.POST)
            if form_partner.is_valid():
                form_partner.save(user_id(request))
                messages.info(request, 'Страница партера создана')
                return HttpResponseRedirect('/partner/{}/'.format(request.POST.get('unp_unn')))
            else:
                data = {
                    'form_partner': form_partner,
                    'user': user,
                    'account_class': 'active',
                    'login': True,
                }
                data.update(csrf(request))
                return render(request, 'partner_add.html', data)
        else:
            form_partner = FormPatrner()
            data = {
                'form_partner': form_partner,
                'user': user,
                'account_class': 'active',
                'login': True,
            }
            data.update(csrf(request))
            return render(request, 'partner_add.html', data)
    else:
        return HttpResponseRedirect('/user/login/')


def parther_page(request, unp_unn):
    '''
    страница партнера
    '''
    if is_login(request):
        user = User.objects.get(id=user_id(request))
        try:
            partner = user.users.get(unp_unn=int(unp_unn), active=True)
        except Exception:
            pass
        data = {
            'login': True,
            'user': user,
            'account_class': 'active',
        }
        if partner:
            data['partner'] = partner
            data['partner_admin'] = True
        else:
            try:
                data['partner'] = Partner.objects.get(
                    unp_unn=int(unp_unn)
                )
            except Partner.DoesNotExist:
                raise Http404
        data.update(csrf(request))
        return render(request, 'partner_page.html', data)
    else:
        return HttpResponseRedirect('/user/login/')


def admin(request, unp_unn):
    '''
    добавление администратора партнерской страницы
    '''
    if is_login(request):
        try:
            partner = Partner.objects.get(
                unp_unn=int(unp_unn),
                active=True
            )
        except Partner.DoesNotExist:
            raise Http404
        user = User.objects.get(id=user_id(request))
        if user not in partner.user.all():
            raise Http404
        if request.method == 'POST':
            # Если поиск по логину
            if request.POST.get('login_search'):
                form_login_search = LoginSearch(request.POST)
                if form_login_search.is_valid():
                    cleaned_data = form_login_search.clean()
                    cache.set(
                        'search_one_user_{}'.format(user_id(request)),
                        cleaned_data.get('user'),
                        1
                    )
                    return HttpResponseRedirect(
                        '/partner/{}/admin/'.format(unp_unn)
                    )
                else:
                    form_data_search = DataSearch()
                    data = {
                        'login': True,
                        'name_server': request.META['SERVER_NAME'],
                        'partner': partner,
                        'user': user,
                        'account_class': 'active',
                        'form_data_search': form_data_search,
                        'form_login_search': form_login_search,
                    }
                    if user in partner.user.all():
                        data['partner_admin'] = True
                    else:
                        raise Http404
                    data.update(csrf(request))
                    return render(request, 'partner_admin.html', data)
            # конец поиска по логину
            elif request.POST.get('data_search'):
                users = False
                if request.POST.get('city_id'):
                    users = User.objects.filter(
                        city_id=request.POST.get('city_id'))
                elif request.POST.get('district_id'):
                    users = User.objects.filter(
                        district_id=request.POST.get('district_id'))
                elif request.POST.get('region_id'):
                    users = User.objects.filter(
                        region_id=request.POST.get('region_id'))
                elif request.POST.get('country_id'):
                    users = User.objects.filter(
                        country_id=request.POST.get('country_id'))
                if users:
                    if request.POST.get('name'):
                        tmp = users.filter(
                            name__icontains=request.POST.get('name')
                        )
                        if tmp:
                            users = tmp
                            del tmp
                    if request.POST.get('family'):
                        tmp = users.filter(
                            family__icontains=request.POST.get('family')
                        )
                        if tmp:
                            users = tmp
                            del tmp
                    if request.POST.get('email'):
                        tmp = users.filter(
                            email__icontains=request.POST.get('email')
                        )
                        if tmp:
                            users = tmp
                            del tmp
                    if request.POST.get('telephone'):
                        tmp = users.filter(
                            telephone__icontains=request.POST.get('telephone')
                        )
                        if tmp:
                            users = tmp
                            del tmp
                if users:
                    cache.set(
                        'search_users_{}'.format(user_id(request)),
                        users,
                        1
                    )
                else:
                    messages.info(request, 'По вашему запросу ничего не найдено')
                return HttpResponseRedirect(
                    '/partner/{}/admin/'.format(unp_unn)
                )
            elif request.POST.get('user_add'):
                fields = {}
                for field in request.POST:
                    fields[field] = request.POST.get(field)
                del fields['csrfmiddlewaretoken']
                del fields['user_add']
                if fields:
                    for user_login in fields:
                        user_add = User.objects.get(login=user_login)
                        partner.user.add(user_add)
                    partner.save()
                    messages.info(request, 'Выбранные пользователи добавлены')
                return HttpResponseRedirect(
                    '/partner/{}/admin/'.format(unp_unn)
                )
        else:
            form_login_search = LoginSearch()
            form_data_search = DataSearch()
            data = {
                'login': True,
                'name_server': request.META['SERVER_NAME'],
                'partner': partner,
                'user': user,
                'account_class': 'active',
                'form_data_search': form_data_search,
                'form_login_search': form_login_search,
                'found_user': cache.get('search_one_user_{}'.format(
                    user_id(request))),
                'found_users': cache.get('search_users_{}'.format(
                    user_id(request)))
            }
            if user in partner.user.all():
                data['partner_admin'] = True
            else:
                raise Http404
            data.update(csrf(request))
            return render(request, 'partner_admin.html', data)
    else:
        return HttpResponseRedirect('/user/login/')


def delete_admin(request, unp_unn, login):
    '''
    удаление администратора партнерской страницы
    '''
    if is_login(request):
        try:
            partner = Partner.objects.get(
                unp_unn=int(unp_unn),
                active=True
            )
        except Partner.DoesNotExist:
            raise Http404
        user_admin = User.objects.get(id=user_id(request))
        if user_admin not in partner.user.all():
            raise Http404
        user = User.objects.get(login=login)
        if user in partner.user.all():
            partner.user.remove(user)
            partner.save()
        else:
            raise Http404
        return HttpResponseRedirect(
            '/partner/{}/admin/'.format(unp_unn)
        )
    else:
        return HttpResponseRedirect('/user/login/')


def edit(request, unp_unn):
    '''
    редактирование партнерской страницы
    '''
    if is_login(request):
        try:
            partner = Partner.objects.get(
                unp_unn=int(unp_unn),
                active=True
            )
        except Partner.DoesNotExist:
            raise Http404
        user = User.objects.get(id=user_id(request))
        if user not in partner.user.all():
            raise Http404
        if request.method == 'POST':
            form_partner = FormPatrnerEdit(request.POST)
            if form_partner.is_valid():
                cleaned_data = form_partner.clean()
                partner.contact_person = cleaned_data.get('contact_person')
                partner.thelephones = cleaned_data.get('thelephones')
                partner.email = cleaned_data.get('email')
                partner.country_id = cleaned_data.get('country_id')
                partner.region_id = cleaned_data.get('region_id')
                partner.district_id = cleaned_data.get('district_id')
                partner.city_id = cleaned_data.get('city_id')
                partner.street = cleaned_data.get('street')
                partner.save()
                messages.info(request, 'Данные изменены')
                return HttpResponseRedirect('/partner/{}/'.format(partner.unp_unn))
            else:
                data = {
                    'user': user,
                    'account_class': 'active',
                    'login': True,
                    'form_partner': form_partner,
                    'partner': partner,
                }
                data.update(csrf(request))
                return render(request, 'partner_add.html', data)
        else:
            initial_data = {
                'contact_person': partner.contact_person,
                'thelephones': partner.thelephones,
                'email': partner.email,
                'country': partner.country.name_ru,
                'region': partner.region.name_ru,
                'district': partner.district.name_ru,
                'city': partner.city.name_ru,
                'street': partner.street,
                'country_id': partner.country_id,
                'region_id': partner.region_id,
                'district_id': partner.district_id,
                'city_id': partner.city_id,
            }
            form_partner = FormPatrnerEdit(initial=initial_data)
            data = {
                'user': user,
                'account_class': 'active',
                'login': True,
                'form_partner': form_partner,
                'partner': partner,
            }
            data.update(csrf(request))
            return render(request, 'partner_edit.html', data)
    else:
        return HttpResponseRedirect('/user/login/')


def delete(request, unp_unn):
    '''
    удаление (скрытие) партнерской страницы
    '''
    if is_login(request):
        try:
            partner = Partner.objects.get(
                unp_unn=int(unp_unn),
                active=True
            )
        except Partner.DoesNotExist:
            raise Http404
        user = User.objects.get(id=user_id(request))
        if user not in partner.user.all():
            raise Http404
        if request.method == 'POST':
            form_del_partner = DelPartner(request.POST)
            if form_del_partner.is_valid():
                partner.active = False
                partner.save()
                return HttpResponseRedirect('/partner/all/')
            else:
                data = {
                    'user': user,
                    'account_class': 'active',
                    'login': True,
                    'partner': partner,
                    'form_del_partner': form_del_partner,
                }
                data.update(csrf(request))
                return render(request, 'partner_delete.html', data)
        else:
            form_del_partner = DelPartner(initial={'user_id': user_id(request)})
            data = {
                'user': user,
                'account_class': 'active',
                'login': True,
                'partner': partner,
                'form_del_partner': form_del_partner,
            }
            data.update(csrf(request))
            return render(request, 'partner_delete.html', data)
    else:
        return HttpResponseRedirect('/user/login/')


'''
Точки в кабинете партнера
...............................................
..00000......0000....00..000.....00....0000....
..00..00...00....00......0000....00..00....00..
..00...00..00....00..00..00.00...00..00........
..00..00...00....00..00..00..00..00...000000...
..00000....00....00..00..00...00.00........00..
..00.......00....00..00..00....0000..00....00..
..00.........0000....00..00.....000....0000....
...............................................
'''


def points(request, unp_unn, page):
    '''
    все точки партнера
    '''
    if is_login(request):
        try:
            partner = Partner.objects.get(
                unp_unn=int(unp_unn),
                active=True
            )
        except Partner.DoesNotExist:
            raise Http404
        user = User.objects.get(id=user_id(request))
        if user not in partner.user.all():
            raise Http404
        count_pages = count_page(
            Point.objects.filter(partner_id=partner.id).count(),
            COUNT_ELEMENTS
        )
        start = int(page) * COUNT_ELEMENTS - COUNT_ELEMENTS
        finish = start + COUNT_ELEMENTS
        points = Point.objects.filter(partner_id=partner.id).order_by('-id')[start:finish]
        data = {
            'user': user,
            'account_class': 'active',
            'login': True,
            'partner': partner,
            'points': points,
            'pages': get_html_pages(
                int(page),
                count_pages,
                '/partner/{}/points/all/'.format(unp_unn)
            ),
        }
        data.update(csrf(request))
        return render(request, 'points/points_all.html', data)
    else:
        return HttpResponseRedirect('/user/login/')


def point_filter_servis(request, unp_unn, servis, page):
    '''
    фильтр точек по названию сервиса
    '''
    if is_login(request):
        try:
            partner = Partner.objects.get(
                unp_unn=int(unp_unn),
                active=True
            )
        except Partner.DoesNotExist:
            raise Http404
        user = User.objects.get(id=user_id(request))
        if user not in partner.user.all():
            raise Http404
        servis = servis.replace('_', ' ')
        count_pages = count_page(
            Point.objects.filter(
                partner_id=partner.id,
                servis__name_en=servis
            ).count(),
            COUNT_ELEMENTS
        )
        start = int(page) * COUNT_ELEMENTS - COUNT_ELEMENTS
        finish = start + COUNT_ELEMENTS
        points = Point.objects.filter(
            partner_id=partner.id,
            servis__name_en=servis
        ).order_by('-id')[start:finish]
        data = {
            'user': user,
            'account_class': 'active',
            'login': True,
            'partner': partner,
            'points': points,
            'pages': get_html_pages(
                int(page),
                count_pages,
                '/partner/{0}/points/servis/{1}/'.format(
                    unp_unn,
                    servis.replace(' ', '_').lower()
                )
            ),
            'filter': True,
        }
        data.update(csrf(request))
        return render(request, 'points/points_all.html', data)
    else:
        return HttpResponseRedirect('/user/login/')


def point_filter_country(request, unp_unn, country, page):
    '''
    фильтр точек по названию страны
    '''
    if is_login(request):
        try:
            partner = Partner.objects.get(
                unp_unn=int(unp_unn),
                active=True
            )
        except Partner.DoesNotExist:
            raise Http404
        user = User.objects.get(id=user_id(request))
        if user not in partner.user.all():
            raise Http404
        country = country.replace('_', ' ')
        count_pages = count_page(
            Point.objects.filter(
                partner_id=partner.id,
                country__name_en=country
            ).count(),
            COUNT_ELEMENTS
        )
        start = int(page) * COUNT_ELEMENTS - COUNT_ELEMENTS
        finish = start + COUNT_ELEMENTS
        points = Point.objects.filter(
            partner_id=partner.id,
            country__name_en=country
        ).order_by('-id')[start:finish]
        data = {
            'user': user,
            'account_class': 'active',
            'login': True,
            'partner': partner,
            'points': points,
            'pages': get_html_pages(
                int(page),
                count_pages,
                '/partner/{0}/points/country/{1}/'.format(
                    unp_unn,
                    country.replace(' ', '_').lower()
                )
            ),
            'filter': True,
        }
        data.update(csrf(request))
        return render(request, 'points/points_all.html', data)
    else:
        return HttpResponseRedirect('/user/login/')


def point_filter_region(request, unp_unn, region, page):
    '''
    фильтр точек по названию региона
    '''
    if is_login(request):
        try:
            partner = Partner.objects.get(
                unp_unn=int(unp_unn),
                active=True
            )
        except Partner.DoesNotExist:
            raise Http404
        user = User.objects.get(id=user_id(request))
        if user not in partner.user.all():
            raise Http404
        region = region.replace('_', ' ')
        count_pages = count_page(
            Point.objects.filter(
                partner_id=partner.id,
                region__name_en=region
            ).count(),
            COUNT_ELEMENTS
        )
        start = int(page) * COUNT_ELEMENTS - COUNT_ELEMENTS
        finish = start + COUNT_ELEMENTS
        points = Point.objects.filter(
            partner_id=partner.id,
            region__name_en=region
        ).order_by('-id')[start:finish]
        data = {
            'user': user,
            'account_class': 'active',
            'login': True,
            'partner': partner,
            'points': points,
            'pages': get_html_pages(
                int(page),
                count_pages,
                '/partner/{0}/points/region/{1}/'.format(
                    unp_unn,
                    region.replace(' ', '_').lower()
                )
            ),
            'filter': True,
        }
        data.update(csrf(request))
        return render(request, 'points/points_all.html', data)
    else:
        return HttpResponseRedirect('/user/login/')


def point_add(request, unp_unn):
    '''
    добавление новой точки
    '''
    if is_login(request):
        try:
            partner = Partner.objects.get(
                unp_unn=int(unp_unn),
                active=True
            )
        except Partner.DoesNotExist:
            raise Http404
        user = User.objects.get(id=user_id(request))
        if user not in partner.user.all():
            raise Http404
        if request.method == 'POST':
            if cache.get('back_add_{}'.format(user_id(request))) is not None:
                back = cache.get('back_add_{}'.format(user_id(request)))
            else:
                back = '/partner/{}/points/all/1/'.format(unp_unn)
            form_add_point = AddPoint(request.POST)
            if form_add_point.is_valid():
                form_add_point.save(partner.id)
                messages.info(request, 'Точка успешно добавлена на карту')
                return HttpResponseRedirect(back)
            else:
                cache.set(
                    'back_add_{}'.format(user_id(request)),
                    back,
                    1200
                )
                data = {
                    'user': user,
                    'account_class': 'active',
                    'login': True,
                    'partner': partner,
                    'back': back,
                    'form_add_point': form_add_point,
                }
                data.update(csrf(request))
                return render(request, 'points/point_add.html', data)
        else:
            try:
                back = request.META['HTTP_REFERER']
                cache.set(
                    'back_add_{}'.format(user_id(request)),
                    back,
                    1200
                )
            except KeyError:
                back = False
            form_add_point = AddPoint()
            data = {
                'user': user,
                'account_class': 'active',
                'login': True,
                'partner': partner,
                'back': back,
                'form_add_point': form_add_point,
            }
            data.update(csrf(request))
            return render(request, 'points/point_add.html', data)
    else:
        return HttpResponseRedirect('/user/login/')


def point_view(request, id_point):
    # def point_view(request, unp_unn, id_point):
    '''
    просмотр точки
    '''
    # if is_login(request):
    point = Point.objects.get(id=int(id_point))
    partner = point.partner
    # try:
    #     partner = Partner.objects.get(
    #         unp_unn=int(unp_unn),
    #         active=True
    #     )
    # except Partner.DoesNotExist:
    #     raise Http404
    # user = User.objects.get(id=user_id(request))
    # if user not in partner.user.all():
    #     raise Http404
    try:
        back = request.META['HTTP_REFERER']
    except KeyError:
        back = '/partner/{}/points/all/1/'.format(partner.unp_unn)
    point.time_work_in_html()
    data = {
        # 'user': user,
        'account_class': 'active',
        'login': True,
        'partner': partner,
        'back': back,
        'point': point,
    }
    data.update(csrf(request))
    return render(request, 'points/point_view.html', data)
    # else:
    #     return HttpResponseRedirect('/user/login/')


def point_edit(request, unp_unn, id_point):
    '''
    редактирование данных точки
    '''
    if is_login(request):
        try:
            partner = Partner.objects.get(
                unp_unn=int(unp_unn),
                active=True
            )
        except Partner.DoesNotExist:
            raise Http404
        user = User.objects.get(id=user_id(request))
        point = Point.objects.get(id=int(id_point))
        if user not in partner.user.all():
            raise Http404
        if request.method == 'POST':
            if cache.get('back_edit_{}'.format(user_id(request))) is not None:
                back = cache.get('back_edit_{}'.format(user_id(request)))
            else:
                back = '/partner/{}/points/all/1/'.format(unp_unn)
            form_edit_point = AddPoint(request.POST)
            if form_edit_point.is_valid():
                form_edit_point.update(point.id)
                messages.info(request, 'Данные изменены')
                return HttpResponseRedirect(back)
            else:
                cache.set(
                    'back_edit_{}'.format(user_id(request)),
                    back,
                    1200
                )
                data = {
                    'user': user,
                    'account_class': 'active',
                    'login': True,
                    'partner': partner,
                    'back': back,
                    'form_edit_point': form_edit_point,
                    'point': point,
                }
                data.update(csrf(request))
                return render(request, 'points/point_edit.html', data)
        else:
            try:
                back = request.META['HTTP_REFERER']
                cache.set(
                    'back_edit_{}'.format(user_id(request)),
                    back,
                    1200
                )
            except KeyError:
                back = '/partner/{}/points/all/1/'.format(unp_unn)
            form_edit_point = AddPoint(initial={
                'country': point.country,
                'region': point.region,
                'district': point.district,
                'city': point.city,
                'servis': point.servis,
                'name': point.name,
                'transport': point.transport,
                'country_id': point.country_id,
                'region_id': point.region_id,
                'district_id': point.district_id,
                'city_id': point.city_id,
                'street': point.street,
                'time_work': point.time_work,
                'thelephones': point.thelephones,
                'url': point.url,
                'desc': point.desc,
                'lat': point.lat,
                'lon': point.lon,
            })
            data = {
                'user': user,
                'account_class': 'active',
                'login': True,
                'partner': partner,
                'back': back,
                'form_edit_point': form_edit_point,
                'point': point,
            }
            data.update(csrf(request))
            return render(request, 'points/point_edit.html', data)
    else:
        return HttpResponseRedirect('/user/login/')


def point_delete(request, unp_unn, id_point):
    '''
    удаление точки
    '''
    if is_login(request):
        try:
            partner = Partner.objects.get(
                unp_unn=int(unp_unn),
                active=True
            )
        except Partner.DoesNotExist:
            raise Http404
        user = User.objects.get(id=user_id(request))
        if user not in partner.user.all():
            raise Http404
        try:
            back = request.META['HTTP_REFERER']
        except KeyError:
            back = '/partner/{}/points/all/1/'.format(unp_unn)
        point = Point.objects.get(id=int(id_point))
        if point.partner_id != partner.id:
            raise Http404
        else:
            cache.set(
                'point_{0}_{1}'.format(unp_unn, id_point),
                point,
                2592000
            )
            point.delete()
            return HttpResponseRedirect(back)
    else:
        return HttpResponseRedirect('/user/login/')


def point_hide(request, unp_unn, id_point):
    '''
    скрытие точки
    '''
    if is_login(request):
        try:
            partner = Partner.objects.get(
                unp_unn=int(unp_unn),
                active=True
            )
        except Partner.DoesNotExist:
            raise Http404
        user = User.objects.get(id=user_id(request))
        if user not in partner.user.all():
            raise Http404
        try:
            back = request.META['HTTP_REFERER']
        except KeyError:
            back = '/partner/{}/points/all/1/'.format(unp_unn)
        point = Point.objects.get(id=int(id_point))
        if point.partner_id != partner.id:
            raise Http404
        else:
            point.active = False
            point.save()
            return HttpResponseRedirect(back)
    else:
        return HttpResponseRedirect('/user/login/')


def point_visible(request, unp_unn, id_point):
    if is_login(request):
        try:
            partner = Partner.objects.get(
                unp_unn=int(unp_unn),
                active=True
            )
        except Partner.DoesNotExist:
            raise Http404
        user = User.objects.get(id=user_id(request))
        if user not in partner.user.all():
            raise Http404
        try:
            back = request.META['HTTP_REFERER']
        except KeyError:
            back = '/partner/{}/points/all/1/'.format(unp_unn)
        point = Point.objects.get(id=int(id_point))
        if point.partner_id != partner.id:
            raise Http404
        else:
            point.active = True
            point.save()
            return HttpResponseRedirect(back)
    else:
        return HttpResponseRedirect('/user/login/')
