from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def floatformat(value, decimal_places=2):
    return f"{value:.{decimal_places}f}"