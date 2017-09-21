from django.shortcuts import render
from django.template.context_processors import csrf


def forum_home(request):
    data = {}
    # это коментарий
    data.update(csrf(request))
    return render(request, 'home_forum.html', data)
