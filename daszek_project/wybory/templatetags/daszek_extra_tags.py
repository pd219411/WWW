from django import template

register = template.Library()

#@register.filter(name='daszek_test_tag')
@register.filter
def daszek_test_tag(value, arg):
    """Removes all values of arg from the given string"""
    return "TEST TAG"
