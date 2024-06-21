from django import template


register = template.Library()


@register.filter
def discounted_price(price, discount_percentage):

    discounted = price * (1 - discount_percentage / 100)

    return f"{discounted:.2f}"
