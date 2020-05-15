from django import template

from cart.models import Order
register = template.Library()


@register.filter
def cart_item_count(user ):
    if user.is_authenticated:
        qs = Order.objects.filter(user =user , orderd =False)
        if qs:
            return qs[0].items.count()
    

    return 0
