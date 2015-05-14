from django import template

import wybory.daszek_common

register = template.Library()

#@register.filter(name='daszek_test_tag')
@register.filter
def daszek_test_tag(value, arg):
	return "TEST TAG" + value + " ^ " + str(arg + 100)

@register.filter
def daszek_modification_timestamp(value):
	return wybory.daszek_common.datetime_to_string(value)
