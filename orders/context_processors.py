from .models import Cart
from accounts.models import CustomerProfile

def cart_count(request):
    cart_count = 0
    if request.user.is_authenticated and hasattr(request.user, 'customer_profile'):
        try:
            customer_profile = request.user.customer_profile
            cart, created = Cart.objects.get_or_create(customer=customer_profile)
            cart_count = cart.item_count
        except CustomerProfile.DoesNotExist:
            cart_count = 0
    return {'cart_count': cart_count} 