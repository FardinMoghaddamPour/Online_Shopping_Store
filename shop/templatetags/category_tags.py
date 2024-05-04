from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='show_subcategories')
def show_subcategories(category):
    subcategories = category.subcategories.all()
    if not subcategories:
        return ''
    html = '<div class="ml-4">'
    for sub in subcategories:
        sub_html = show_subcategories(sub)
        html += f'<p>{sub.name}</p>{sub_html}'
    html += '</div>'
    return mark_safe(html)
