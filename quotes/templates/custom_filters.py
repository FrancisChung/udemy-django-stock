# In your app's templatetags directory (e.g., myapp/templatetags/my_filters.py)
from django import template

register = template.Library()

@register.filter
def contains(value, arg):
    """
    Checks if a string contains a substring.
    Usage: {{ my_string|contains:"substring" }}
    """
    return arg in value