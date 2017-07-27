from django.template.context_processors import csrf
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from project.forms import FeedbackForm
from soyzniki.main.auth import rand_long_int
from project.models import Visitor
from soyzniki.main.auth import get_country_by_ip
from datetime import date


def agreement(request):
    data = {}
    try:
        data['back'] = request.META['HTTP_REFERER']
    except KeyError:
        pass
    data.update(csrf(request))
    return render(request, 'agreement.html', data)


def description(request):
    data = {
        'about_us_class': 'active',
    }
    data.update(csrf(request))
    return render(request, 'description.html', data)


def contacts(request):
    if request.method == 'POST':
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            feedback_form.save()
            messages.info(request, 'Ваше сообщение отправлено')
            return HttpResponseRedirect('/project/contacts/')
        else:
            data = {
                'contacts_class': 'active',
                'feedback_form': feedback_form,
            }
            data.update(csrf(request))
            return render(request, 'contacts.html', data)
    else:
        feedback_form = FeedbackForm()
        data = {
            'contacts_class': 'active',
            'feedback_form': feedback_form,
        }
        data.update(csrf(request))
        return render(request, 'contacts.html', data)


def get_test_cookie(request):
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        try:
            back = request.META['HTTP_REFERER']
        except KeyError:
            back = '/'
        visitor = Visitor()
        visitor.second_id = str(rand_long_int())
        visitor.count_visits = 0
        visitor.date_visit = date.today()
        data_ip = get_country_by_ip(request.META['REMOTE_ADDR'])
        visitor.country = data_ip['country']
        visitor.save()
        response = HttpResponseRedirect(back)
        response.set_cookie(
            'usertoken',
            '{0}{1}'.format(
                visitor.id,
                visitor.second_id
            ),
            max_age = 60 * 60 * 24 * 365,
            path='/'
        )
        return response
