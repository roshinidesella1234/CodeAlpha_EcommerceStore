import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_config.settings')
django.setup()

from django.test.utils import setup_test_environment
setup_test_environment()

from django.test import Client
from django.contrib.auth.models import User
from store.models import Category, Product, Cart, CartItem, Order, OrderItem

def run_tests():
    print("--- STARTING FULL E-COMMERCE END-TO-END VERIFICATION ---")

    client = Client()

    # 1. Test Product Listing Page GET
    res = client.get('/')
    assert res.status_code == 200, f"Expected 200 on catalog home, got {res.status_code}"
    assert res.context['products'].count() > 0, "No products found in context"
    print("[OK] Catalog home page loaded successfully with products.")

    # 2. Test Category Filter GET
    cat = Category.objects.first()
    res = client.get(f'/?category={cat.slug}')
    assert res.status_code == 200
    for p in res.context['products']:
        assert p.category == cat
    print(f"[OK] Category filter ('{cat.name}') applied successfully.")

    # 3. Test Product Detail GET
    prod = Product.objects.first()
    res = client.get(f'/product/{prod.slug}/')
    assert res.status_code == 200
    assert res.context['product'] == prod
    print(f"[OK] Product detail view for '{prod.name}' rendered correctly.")

    # 4. Test Add To Cart (Guest Session)
    initial_stock = prod.stock
    res = client.post(f'/cart/add/{prod.id}/', {'quantity': 2}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    assert res.status_code == 200
    data = res.json()
    assert data['success'] is True
    assert data['cart_total_items'] == 2
    print("[OK] Guest Add to Cart AJAX test passed.")

    # 5. Test Cart Detail GET
    res = client.get('/cart/')
    assert res.status_code == 200
    assert res.context['total_items'] == 2
    print("[OK] Cart view rendered with guest items.")

    # 6. Test User Registration and Cart Merge
    user_data = {
        'username': 'testbuyer',
        'first_name': 'Test',
        'last_name': 'Buyer',
        'email': 'buyer@example.com',
        'password1': 'Pass123456!Secure',
        'password2': 'Pass123456!Secure',
    }
    res = client.post('/register/', user_data)
    assert res.status_code == 302, f"Expected redirect after register, got {res.status_code}"
    user = User.objects.get(username='testbuyer')
    print("[OK] User registration successful.")

    # Check merged cart
    user_cart = Cart.objects.get(user=user)
    assert user_cart.get_total_items() == 2, f"Expected merged cart total 2, got {user_cart.get_total_items()}"
    print("[OK] Guest cart automatically merged into user account upon registration.")

    # 7. Test Checkout Order Placement
    checkout_data = {
        'full_name': 'Test Buyer',
        'email': 'buyer@example.com',
        'address': '123 Innovation Drive',
        'city': 'San Jose',
        'postal_code': '95110',
        'phone': '+1555123456',
    }
    res = client.post('/checkout/', checkout_data)
    assert res.status_code == 302, f"Expected redirect after checkout, got {res.status_code}"
    
    order = Order.objects.filter(user=user).latest('created_at')
    assert order.full_name == 'Test Buyer'
    assert order.items.count() == 1
    assert order.items.first().quantity == 2
    print(f"[OK] Checkout processed. Order #{order.id} created with total ${order.total_price}.")

    # Check stock reduction
    prod.refresh_from_db()
    assert prod.stock == initial_stock - 2, f"Expected stock {initial_stock - 2}, got {prod.stock}"
    print(f"[OK] Stock decremented from {initial_stock} to {prod.stock}.")

    # Check cart emptied
    user_cart.refresh_from_db()
    assert user_cart.get_total_items() == 0
    print("[OK] Shopping cart cleared after order completion.")

    # 8. Test Order History View
    res = client.get('/orders/')
    assert res.status_code == 200
    assert len(res.context['orders']) == 1
    print("[OK] Order history page verified.")

    print("\nALL E-COMMERCE END-TO-END VERIFICATION TESTS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    run_tests()
