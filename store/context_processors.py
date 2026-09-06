from .models import Cart

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
    return cart

def cart_context(request):
    try:
        cart = get_or_create_cart(request)
        return {
            'cart_total_items': cart.get_total_items(),
            'cart_total_price': cart.get_total_price()
        }
    except Exception:
        return {
            'cart_total_items': 0,
            'cart_total_price': 0
        }
