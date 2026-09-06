from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from .forms import UserRegistrationForm, UserLoginForm, CheckoutForm
from .context_processors import get_or_create_cart


def merge_guest_cart_to_user(request, user):
    """Merge guest session cart items into the user's cart upon login/register."""
    session_key = request.session.session_key
    if not session_key:
        return
    try:
        guest_cart = Cart.objects.get(session_key=session_key, user__isnull=True)
        user_cart, _ = Cart.objects.get_or_create(user=user)
        for item in guest_cart.items.all():
            user_item, created = CartItem.objects.get_or_create(
                cart=user_cart,
                product=item.product,
                defaults={'quantity': item.quantity}
            )
            if not created:
                user_item.quantity += item.quantity
                user_item.save()
        guest_cart.delete()
    except Cart.DoesNotExist:
        pass


def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)

    category_slug = request.GET.get('category')
    search_query = request.GET.get('search')
    selected_category = None

    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query or '',
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)


def cart_detail(request):
    cart = get_or_create_cart(request)
    items = cart.items.select_related('product').all()
    context = {
        'cart': cart,
        'items': items,
        'total_price': cart.get_total_price(),
        'total_items': cart.get_total_items(),
    }
    return render(request, 'store/cart.html', context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    if not product.in_stock:
        messages.error(request, f"Sorry, '{product.name}' is currently out of stock.")
        return redirect('product_detail', slug=product.slug)

    cart = get_or_create_cart(request)
    
    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1

    if quantity < 1:
        quantity = 1

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        if cart_item.quantity + quantity > product.stock:
            messages.warning(request, f"Only {product.stock} units of '{product.name}' available in stock.")
            cart_item.quantity = product.stock
        else:
            cart_item.quantity += quantity
    else:
        cart_item.quantity = min(quantity, product.stock)
    
    cart_item.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f"Added '{product.name}' to your cart!",
            'cart_total_items': cart.get_total_items(),
            'cart_total_price': float(cart.get_total_price()),
        })

    messages.success(request, f"Added '{product.name}' to your shopping cart!")
    return redirect('cart_detail')


def update_cart(request, item_id):
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    action = request.POST.get('action')
    try:
        new_quantity = int(request.POST.get('quantity', cart_item.quantity))
    except (ValueError, TypeError):
        new_quantity = cart_item.quantity

    if action == 'increase':
        new_quantity = cart_item.quantity + 1
    elif action == 'decrease':
        new_quantity = cart_item.quantity - 1

    if new_quantity <= 0:
        cart_item.delete()
        message = f"Removed '{cart_item.product.name}' from your cart."
    else:
        if new_quantity > cart_item.product.stock:
            new_quantity = cart_item.product.stock
            messages.warning(request, f"Maximum stock of {cart_item.product.stock} reached.")
        cart_item.quantity = new_quantity
        cart_item.save()
        message = f"Updated quantity for '{cart_item.product.name}'."

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        item_subtotal = float(cart_item.get_subtotal()) if new_quantity > 0 else 0.0
        return JsonResponse({
            'success': True,
            'message': message,
            'item_quantity': cart_item.quantity if new_quantity > 0 else 0,
            'item_subtotal': item_subtotal,
            'cart_total_items': cart.get_total_items(),
            'cart_total_price': float(cart.get_total_price()),
        })

    messages.success(request, message)
    return redirect('cart_detail')


def remove_from_cart(request, item_id):
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    product_name = cart_item.product.name
    cart_item.delete()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f"Removed '{product_name}' from cart.",
            'cart_total_items': cart.get_total_items(),
            'cart_total_price': float(cart.get_total_price()),
        })

    messages.info(request, f"Removed '{product_name}' from your cart.")
    return redirect('cart_detail')


def checkout(request):
    cart = get_or_create_cart(request)
    items = cart.items.select_related('product').all()

    if not items:
        messages.warning(request, "Your shopping cart is empty. Add products before checkout.")
        return redirect('product_list')

    if not request.user.is_authenticated:
        messages.info(request, "Please register or log in to complete your order checkout.")
        return redirect(f"/login/?next=/checkout/")

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = cart.get_total_price()
            order.status = 'Completed'
            order.save()

            # Create OrderItems and adjust product stock
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    price=item.product.price,
                    quantity=item.quantity
                )
                # Decrement stock
                product = item.product
                product.stock = max(0, product.stock - item.quantity)
                product.save()

            # Clear cart
            cart.items.all().delete()

            messages.success(request, f"Order #{order.id} placed successfully!")
            return redirect('order_success', order_id=order.id)
    else:
        initial_data = {
            'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'email': request.user.email,
        }
        form = CheckoutForm(initial=initial_data)

    context = {
        'form': form,
        'cart': cart,
        'items': items,
        'total_price': cart.get_total_price(),
    }
    return render(request, 'store/checkout.html', context)


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {'order': order}
    return render(request, 'store/order_success.html', context)


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    context = {'orders': orders}
    return render(request, 'store/order_history.html', context)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('product_list')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            merge_guest_cart_to_user(request, user)
            login(request, user)
            messages.success(request, f"Welcome to CodeAlpha Store, {user.username}! Your account has been created.")
            return redirect('product_list')
    else:
        form = UserRegistrationForm()

    return render(request, 'store/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('product_list')

    next_url = request.GET.get('next', 'product_list')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            merge_guest_cart_to_user(request, user)
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect(next_url or 'product_list')
    else:
        form = UserLoginForm()

    return render(request, 'store/login.html', {'form': form, 'next': next_url})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('product_list')
