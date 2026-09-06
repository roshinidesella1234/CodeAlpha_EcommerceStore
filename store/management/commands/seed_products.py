from django.core.management.base import BaseCommand
from django.utils.text import slugify
from store.models import Category, Product

class Command(BaseCommand):
    help = 'Seeds initial product categories and items into the database'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding sample product data...")

        categories_data = [
          {'name': 'Electronics'},
          {'name': 'Audio & Sound'},
          {'name': 'Wearables'},
          {'name': 'Accessories'},
          {'name': 'Workstation'},
        ]

        cat_objs = {}
        for cdata in categories_data:
            cat, created = Category.objects.get_or_create(
                name=cdata['name'],
                defaults={'slug': slugify(cdata['name'])}
            )
            cat_objs[cdata['name']] = cat
            if created:
                self.stdout.write(f"Created category: {cat.name}")

        products_data = [
            {
                'name': 'Wireless Active Noise-Canceling Headphones',
                'category': 'Audio & Sound',
                'price': 199.99,
                'stock': 25,
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80',
                'description': 'Premium over-ear wireless headphones featuring active noise cancellation, 30-hour battery life, immersive acoustic clarity, and comfortable memory foam ear cushions.'
            },
            {
                'name': 'Ultra-Slim Mechanical Wireless Keyboard',
                'category': 'Workstation',
                'price': 129.50,
                'stock': 15,
                'image_url': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&auto=format&fit=crop&q=80',
                'description': 'Tactile low-profile mechanical keyboard with per-key RGB backlighting, dual Bluetooth/USB-C connectivity, and aircraft-grade aluminum top plate.'
            },
            {
                'name': 'Smart Fitness Tracker & Heart Rate Watch',
                'category': 'Wearables',
                'price': 89.99,
                'stock': 40,
                'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&auto=format&fit=crop&q=80',
                'description': 'Water-resistant smartwatch featuring continuous heart rate monitoring, sleep analysis, 14 sport tracking modes, and up to 10 days of battery performance.'
            },
            {
                'name': 'Ergonomic Precision Wireless Mouse',
                'category': 'Workstation',
                'price': 69.99,
                'stock': 30,
                'image_url': 'https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=800&auto=format&fit=crop&q=80',
                'description': 'Advanced ergonomic mouse engineered for maximum comfort, high-precision 4000 DPI tracking sensor, hyper-fast scroll wheel, and multi-device pairing.'
            },
            {
                'name': 'Portable Hi-Fi Bluetooth Speaker',
                'category': 'Audio & Sound',
                'price': 119.00,
                'stock': 18,
                'image_url': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=800&auto=format&fit=crop&q=80',
                'description': 'Rugged IPX7 waterproof portable speaker delivering punchy 360-degree bass response, dual passive radiators, and continuous 20-hour wireless playback.'
            },
            {
                'name': '4K Ultra HD Action Camera',
                'category': 'Electronics',
                'price': 249.99,
                'stock': 12,
                'image_url': 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800&auto=format&fit=crop&q=80',
                'description': 'Compact 4K 60fps action camera equipped with smooth optical image stabilization, waterproof housing down to 30m, and dual LCD screens for vlogging.'
            },
            {
                'name': 'USB-C Multi-Port Hub Adapter (8-in-1)',
                'category': 'Accessories',
                'price': 45.99,
                'stock': 50,
                'image_url': 'https://images.unsplash.com/photo-1544652478-6653e09f18a2?w=800&auto=format&fit=crop&q=80',
                'description': 'Sleek aluminum USB-C hub providing 4K HDMI Output, 100W Power Delivery, SD/MicroSD card readers, and 3x USB 3.0 high-speed data transfer ports.'
            },
            {
                'name': 'Minimalist Waterproof Laptop Backpack',
                'category': 'Accessories',
                'price': 79.50,
                'stock': 22,
                'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800&auto=format&fit=crop&q=80',
                'description': 'Durable water-resistant backpack featuring padded protection for up to 16-inch laptops, hidden anti-theft security pocket, and built-in USB charging port.'
            }
        ]

        for pdata in products_data:
            cat = cat_objs[pdata['category']]
            prod, created = Product.objects.get_or_create(
                slug=slugify(pdata['name']),
                defaults={
                    'name': pdata['name'],
                    'category': cat,
                    'price': pdata['price'],
                    'stock': pdata['stock'],
                    'image_url': pdata['image_url'],
                    'description': pdata['description'],
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(f"Added product: {prod.name}")

        self.stdout.write(self.style.SUCCESS("Successfully seeded sample product data!"))
