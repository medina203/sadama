from django import template

register = template.Library()


@register.filter
def cop(value):
    try:
        val = float(value)
        integer = int(val)
        integer_str = f"{integer:,}".replace(",", ".")
        return f"$ {integer_str}"
    except (ValueError, TypeError):
        return "$ 0"
