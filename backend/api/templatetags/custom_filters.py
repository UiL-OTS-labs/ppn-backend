from django import template
import re

register = template.Library()

@register.filter
def remove_bold_tags(value):
    """Verwijdert <b> en <strong> tags uit een string of object met __str__"""
    if not value:
        return ''
    text = str(value)  # force to string
    return re.sub(r'</?b>|</?strong>', '', text, flags=re.IGNORECASE)
