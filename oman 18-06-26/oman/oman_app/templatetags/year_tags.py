from django import template
from datetime import datetime

register = template.Library()

@register.filter
def get_years(start_year):
    current_year = datetime.now().year
    return range(current_year, int(start_year) - 1, -1)
