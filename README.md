<<<<<<< HEAD
# CodeAlpha Full-Stack E-Commerce Store

A responsive, feature-rich full-stack E-Commerce web application built with **Django**, **SQLite**, **HTML5**, **CSS3**, and **JavaScript**.

---

## 🚀 Features Built

- 🛍️ **Product Catalog Page**: Responsive product grid layout, live search bar, category navigation bar, stock badges, and price indicators.
- 🔍 **Product Detail Page**: Full product breakdown, stock availability badge, quantity increment/decrement controls, AJAX Add-to-Cart, and related product recommendations.
- 🛒 **Shopping Cart**: Dynamic itemized cart table, item subtotal calculation, quantity modification, single-item removal, clear cart, order summary breakdown (Subtotal, Shipping, Taxes), and badge counter in navbar.
- 🔐 **User Authentication**: User registration with input validation, login, logout, and guest session cart auto-merging upon authentication.
- 💳 **Checkout & Order Processing**: Shipping/billing details form, simulated payment gateway approval, itemized order record creation, automatic stock deduction, and cart clearing.
- 📜 **Order History**: User order dashboard displaying all past orders with status badges (`Completed`, `Pending`), purchase dates, shipping addresses, and detailed line items.
- 🎨 **Modern Responsive UI**: Custom CSS design system with CSS custom variables, dark/light contrast elements, smooth animations, toast notifications, and mobile responsiveness.

---

## 🛠️ Project Structure

```
codealpha_ecommerce/
├── .venv/                         # Python virtual environment
├── db.sqlite3                     # SQLite database
├── manage.py                      # Django CLI runner
├── test_e2e.py                    # End-to-End automated test suite
├── requirements.txt               # Dependencies file (Django 6.1+)
├── ecommerce_config/              # Project settings & URL routing
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── store/                         # E-commerce Django app
    ├── models.py                  # Category, Product, Cart, CartItem, Order, OrderItem
    ├── views.py                   # Product, Cart, Checkout, Order, Auth logic
    ├── forms.py                   # Registration, Login, Checkout forms
    ├── admin.py                   # Admin dashboard configuration
    ├── urls.py                    # App routes
    ├── context_processors.py      # Global cart badge & navbar total
    ├── static/store/
    │   ├── css/style.css          # Custom styling & responsive layouts
    │   └── js/main.js             # AJAX cart operations & toasts
    ├── templates/store/
    │   ├── base.html              # Shell layout with header & footer
    │   ├── product_list.html      # Catalog grid with search & filters
    │   ├── product_detail.html    # Product specs & quantity selector
    │   ├── cart.html              # Interactive cart
    │   ├── checkout.html          # Order checkout form
    │   ├── order_success.html     # Confirmation receipt
    │   ├── order_history.html     # User past orders list
    │   ├── register.html          # User registration card
    │   └── login.html             # User login card
    └── management/commands/
        └── seed_products.py       # Seed initial categories & catalog
```

---

## 💻 How to Run Locally

### 1. Open Terminal in Project Folder
```bash
cd "C:\Users\D MOUNIKALAKASHMI\.gemini\antigravity\scratch\codealpha_ecommerce"
```

### 2. Activate Virtual Environment
On Windows:
```cmd
.\.venv\Scripts\activate
```

### 3. Run the Development Server
```bash
python manage.py runserver
```

### 4. Open Application in Browser
Go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your web browser.

---

## 🧪 Verification & Testing

To execute the automated end-to-end verification suite testing catalog loading, search, category filtering, cart operations, user registration, cart merging, checkout, stock deduction, and order history:

```bash
python test_e2e.py
```
=======
# CodeAlpha_EcommerceStore
Simple E-commerce Store using HTML, CSS, JS, Django/Express.js
>>>>>>> ca69816c6a287b974fb1bce2e728fd021458c0ba
