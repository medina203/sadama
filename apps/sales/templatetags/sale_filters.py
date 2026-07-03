from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


@register.filter
def cop(value):
    try:
        val = float(value)
        return f"$ {intcomma(f'{val:,.0f}')}"
    except (ValueError, TypeError):
        return "$ 0"
