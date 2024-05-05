from django import template
from django.utils.safestring import mark_safe
from django.urls import reverse

register = template.Library()


@register.filter(name='show_subcategories')
def show_subcategories(category):

    subcategories = category.subcategories.all()

    if not subcategories:
        return ''

    html = '<div class="ml-4">'

    for sub in subcategories:

        url = reverse('shop:category_products', args=[sub.id])
        sub_html = show_subcategories(sub)
        html += f'<p><a href="{url}" class="text-blue-500 hover:text-blue-700">{sub.name}</a></p>{sub_html}'

    html += '</div>'

    return mark_safe(html)
