from django.shortcuts import render
from django.template.context_processors import csrf
from soyzniki.main.pages import count_page, get_html_pages
from news.models import News, Rubric
from bs4 import BeautifulSoup
from django.http import Http404
from soyzniki.main.auth import is_login, user_id
from comments.views import view_comments
from user.models import User


COUNT_ELEMENTS = 8


def link_to_name(string):
    list_string = string.split('_')
    if len(list_string) > 1:
        for line in list_string:
            line.capitalize()
        return ' '.join(list_string)
    else:
        return string.capitalize()


def news(request, page):
    count_pages = count_page(
        News.objects.filter(online=True).count(),
        COUNT_ELEMENTS
    )
    start = int(page) * COUNT_ELEMENTS - COUNT_ELEMENTS
    finish = start + COUNT_ELEMENTS
    all_news = News.objects.filter(online=True)[start:finish]
    rubric = Rubric.objects.filter(active=True)
    all_rubric = []
    html = '<li {0}><a href="/news/rubric/{1}/1/">{2}</a></li>'
    all_rubric.append(
        '<li class="now_rubric"><a href="/news/1/">Все</a></li>'
    )
    for line in rubric:
        all_rubric.append(
            html.format(
                '',
                line.name_en.lower(),
                line.name_ru
            )
        )
    for news in all_news:
        content_html = BeautifulSoup(news.content)
        all_content = content_html.get_text()
        list_content = list(all_content)[0:151]
        news.content = ''.join(list_content)
    data = {
        'all_news': all_news,
        'pages': get_html_pages(int(page), count_pages, '/news/'),
        'login': False,
        'all_rubric': all_rubric,
        'news_class': 'active',
    }
    if is_login(request):
        user = User.objects.get(id=user_id(request))
        data['login'] = True
        data['user'] = user
    data.update(csrf(request))
    return render(request, 'news.html', data)


def rubric(request, rubric, page):
    count_pages = count_page(
        News.objects.filter(rubric__name_en=rubric, online=True).count(),
        COUNT_ELEMENTS
    )
    start = int(page) * COUNT_ELEMENTS - COUNT_ELEMENTS
    finish = start + COUNT_ELEMENTS
    all_news = News.objects.filter(rubric__name_en=rubric, online=True)[start:finish]
    for news in all_news:
        content_html = BeautifulSoup(news.content)
        all_content = content_html.get_text()
        list_content = list(all_content)[0:151]
        news.content = ''.join(list_content)
    rubric_all = Rubric.objects.filter(active=True)
    all_rubric = []
    all_rubric.append('<li><a href="/news/1/">Все</a></li>')
    html = '<li {0}><a href="/news/rubric/{1}/1/">{2}</a></li>'
    for line in rubric_all:
        if line.name_en == link_to_name(rubric):
            all_rubric.append(
                html.format(
                    'class="now_rubric"',
                    line.name_en.lower(),
                    line.name_ru
                )
            )
        else:
            all_rubric.append(
                html.format(
                    '',
                    line.name_en.lower(),
                    line.name_ru
                )
            )
    data = {
        'all_news': all_news,
        'pages': get_html_pages(int(page), count_pages, '/news/'),
        'login': False,
        'all_rubric': all_rubric,
        'news_class': 'active',
    }
    if is_login(request):
        user = User.objects.get(id=user_id(request))
        data['login'] = True
        data['user'] = user
    data.update(csrf(request))
    return render(request, 'news.html', data)


def country(request, country, page):
    count_pages = count_page(
        News.objects.filter(country__name_en=country, online=True).count(),
        COUNT_ELEMENTS
    )
    start = int(page) * COUNT_ELEMENTS - COUNT_ELEMENTS
    finish = start + COUNT_ELEMENTS
    all_news = News.objects.filter(country__name_en=country, online=True)[start:finish]
    for news in all_news:
        content_html = BeautifulSoup(news.content)
        all_content = content_html.get_text()
        list_content = list(all_content)[0:151]
        news.content = ''.join(list_content)
    rubric = Rubric.objects.filter(active=True)
    all_rubric = []
    all_rubric.append('<li><a href="/news/1/">Все</a></li>')
    html = '<li {0}><a href="/news/rubric/{1}/1/">{2}</a></li>'
    for line in rubric:
        all_rubric.append(
            html.format(
                '',
                line.name_en.lower(),
                line.name_ru
            )
        )
    data = {
        'all_news': all_news,
        'pages': get_html_pages(int(page), count_pages, '/news/'),
        'login': False,
        'news_class': 'active',
        'all_rubric': all_rubric
    }
    if is_login(request):
        user = User.objects.get(id=user_id(request))
        data['login'] = True
        data['user'] = user
    data.update(csrf(request))
    return render(request, 'news.html', data)


def one_news(request, news):
    try:
        news = News.objects.get(link=news)
    except News.DoesNotExist:
        raise Http404
    try:
        back = request.META['HTTP_REFERER']
    except KeyError:
        back = False
    images = news.image.all()
    content = news.content.split('\n')
    img_html = '<img src="/media/{0}" alt="{1}" />'
    all_content = []
    for i in range(0, len(images)):
        all_content.append(
            img_html.format(images[i].full_image, images[i].name)
        )
        try:
            all_content.append(
                '{0}\n'.format(content[0])
            )
            del content[0]
        except IndexError:
            all_content.append('\n')
    if len(content):
        all_content.append(
            '\n'.join(content)
        )
    news.content = '\n'.join(all_content)
    comments = view_comments(request, str(News.__module__), str(News.__name__), news.id)
    data = {
        'news': news,
        'back': back,
        'comments': comments,
        'news_class': 'active',
        'login': False
    }
    if is_login(request):
        user = User.objects.get(id=user_id(request))
        data['login'] = True
        data['user'] = user
    data.update(csrf(request))
    return render(request, 'one_news.html', data)
