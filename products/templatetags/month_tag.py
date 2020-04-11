from django import template
register = template.Library()
import calendar


@register.filter()
def month_name(month_number):
    return calendar.month_name[month_number]
