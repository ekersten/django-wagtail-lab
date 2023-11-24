import os

from django import template
from django.conf import settings
from django.templatetags.static import StaticNode

register = template.Library()


@register.simple_tag
def hotreload(app, path):
    if os.path.isfile(os.path.join(settings.BASE_DIR, 'hot')):
        with open(os.path.join(settings.BASE_DIR, 'hot'), 'r') as file:
            base_url = file.read().rstrip()
        return f'{base_url}/{app}/static/{path}'
    else:
        return StaticNode.handle_simple(path)
