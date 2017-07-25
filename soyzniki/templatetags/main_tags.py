# from soyzniki.modelss import Timezone
from django import template
from time import gmtime

register = template.Library()


@register.filter(name='to_link')
def string_to_link(value):
    value = value.replace(' ', '_').lower()
    return value


@register.filter(name='get_time')
def get_time(value):
    try:
        time_h = gmtime(value)
    except ValueError:
        msg = 'Invalid value passed. Unix time is accepted.'
        raise template.TemplateSyntaxError(msg)
    else:
        time_w = '{0}:{1:0<2}'.format(time_h[3], time_h[4])
        return time_w
