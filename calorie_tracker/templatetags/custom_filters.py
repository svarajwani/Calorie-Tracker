from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def round_number(value):
    """Rounds a number to the specified number of decimals."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return value