from django.core.management.base import BaseCommand
from shop.models import Category, Product


class Command(BaseCommand):
    help = "Seed the database with sample products"

    def handle(self, *args, **options):
        categories = {
            "electronics": "Electronics",
            "home": "Home & Living",
            "fashion": "Fashion",
            "accessories": "Accessories",
        }

        for slug, name in categories.items():
            category, _ = Category.objects.get_or_create(slug=slug, defaults={"name": name})
            self.stdout.write(self.style.SUCCESS(f"Category ready: {category.name}"))

        product_data = [
            {
                "category": "electronics",
                "name": "Aurora Wireless Headphones",
                "slug": "aurora-wireless-headphones",
                "description": "Premium over-ear headphones with deep bass, noise isolation, and crystal-clear audio.",
                "price": "129.99",
                "stock": 25,
                "image": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=900&q=80",
                "featured": True,
            },
            {
                "category": "home",
                "name": "Luna Ceramic Vase",
                "slug": "luna-ceramic-vase",
                "description": "Modern handcrafted vase designed to bring elegance to your home decor.",
                "price": "54.00",
                "stock": 18,
                "image": "https://images.unsplash.com/photo-1503602642458-232111445657?auto=format&fit=crop&w=900&q=80",
                "featured": True,
            },
            {
                "category": "fashion",
                "name": "Harbor Cotton Hoodie",
                "slug": "harbor-cotton-hoodie",
                "description": "A soft everyday hoodie with a relaxed fit and premium cotton comfort.",
                "price": "72.50",
                "stock": 30,
                "image": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?auto=format&fit=crop&w=900&q=80",
                "featured": True,
            },
            {
                "category": "accessories",
                "name": "Sora Leather Wallet",
                "slug": "sora-leather-wallet",
                "description": "Minimal leather wallet with room for cards, cash, and everyday essentials.",
                "price": "39.90",
                "stock": 20,
                "image": "https://images.unsplash.com/photo-1627123424574-724758594e93?auto=format&fit=crop&w=900&q=80",
                "featured": False,
            },
            {
                "category": "electronics",
                "name": "Nimbus Smart Watch",
                "slug": "nimbus-smart-watch",
                "description": "Track health, workouts, notifications, and time in a sleek smartwatch design.",
                "price": "199.00",
                "stock": 15,
                "image": "https://images.unsplash.com/photo-1546868871-7041f2a55e12?auto=format&fit=crop&w=900&q=80",
                "featured": True,
            },
            {
                "category": "home",
                "name": "Solstice Desk Lamp",
                "slug": "solstice-desk-lamp",
                "description": "A minimal desk lamp built with a warm glow and dimmable LED lighting.",
                "price": "68.00",
                "stock": 28,
                "image": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=900&q=80",
                "featured": False,
            },
        ]

        for item in product_data:
            category = Category.objects.get(slug=item["category"])
            product, created = Product.objects.get_or_create(
                slug=item["slug"],
                defaults={
                    "category": category,
                    "name": item["name"],
                    "description": item["description"],
                    "price": item["price"],
                    "stock": item["stock"],
                    "image": item["image"],
                    "featured": item["featured"],
                },
            )
            if not created:
                product.category = category
                product.name = item["name"]
                product.description = item["description"]
                product.price = item["price"]
                product.stock = item["stock"]
                product.image = item["image"]
                product.featured = item["featured"]
                product.save()
            self.stdout.write(self.style.SUCCESS(f"Product ready: {product.name}"))

        self.stdout.write(self.style.SUCCESS("Sample data loaded successfully."))
