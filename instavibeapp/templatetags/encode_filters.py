from django import template
from ..utils import encode_id

register = template.Library()

@register.filter
def encode_id_filter(value):
    return encode_id(value)
