from django import template
from ..models import Blog
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

# @register.simple_tag
# def total_posts():
#     return Blog.objects.count()

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
