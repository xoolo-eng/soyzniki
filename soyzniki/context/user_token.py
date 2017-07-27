from django.conf import settings
from project.models import Visitor
from datetime import date


def bad_redirect(request):
    data = {}
    try:
        request.COOKIES['uservisit']
    except KeyError:
        try:
            browser_id = request.COOKIES['usertoken']
        except KeyError:
            robot = False
            for line in settings.ROBOTS_LIST:
                if line in request.META['HTTP_USER_AGENT']:
                    robot = True
                    break
            if robot:
                pass
            else:
                request.session.set_test_cookie()
                data['redirect'] = '''
                <meta http-equiv="refresh" content="0;/project/get_test_cookie/">
                '''
        else:
            visitor_id = browser_id[0:-20]
            second_id = browser_id[-20:]
            visitor = Visitor.objects.get(id=int(visitor_id), second_id=second_id)
            visitor.count_visits += 1
            visitor.date_visit = date.today()
            visitor.save()
            data['redirect'] = '''
            <script>
                document.cookie = "uservisit=1;path=/";
            </script>
            '''
    return data
