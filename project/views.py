from django.template.context_processors import csrf
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from project.forms import FeedbackForm


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
