from comments.models import Comments
from comments.forms import CommentsForm
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from soyzniki.main.auth import is_login, user_id
from django.template.context_processors import csrf
from django.contrib import messages


def view_comments(request, application, model, record_id):
    all_comments = Comments.objects.filter(
        applications=application,
        model=model,
        record_id=record_id,
        moderation=True
    )
    data = {
        'comment_form': False,
        'all_comments': all_comments
    }
    if is_login(request):
        comment_form = CommentsForm(initial={
            'applications': application,
            'model': model,
            'record_id': record_id,
            'user': user_id(request)
        })
        data['comment_form'] = comment_form
    data.update(csrf(request))
    return render_to_string('comments.html', data)


def add(request):
    try:
        page = request.META['HTTP_REFERER']
    except KeyError:
        page = False
    if page:
        if request.method == 'POST':
            comment_form = CommentsForm(request.POST)
            if comment_form.is_valid():
                comment_form.save()
                messages.info(request, 'Ваш коментарий успешно отправлен')
                messages.info(request, 'После проверки модератором он будет доступен на сайте')
                return HttpResponseRedirect(page)
            else:
                messages.info(request, 'Ошибка добавления коментария')
                messages.info(request, 'Проверьте введенные данные')
                return HttpResponseRedirect(page)
    else:
        messages.info(request, 'Ошибка добавления коментария')
        messages.info(request, 'Проверьте введенные данные')
        return HttpResponseRedirect('/')
