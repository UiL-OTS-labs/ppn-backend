from django import template
import re

register = template.Library()

@register.filter
def remove_bold_tags(value):
    """Verwijdert <b> en <strong> tags uit een string"""
    if not value:
        return ''
    return re.sub(r'</?b>|</?strong>', '', value, flags=re.IGNORECASE)
