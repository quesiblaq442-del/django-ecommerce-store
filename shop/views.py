from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
import stripe # type: ignore
from django.conf import settings
from .forms import CheckoutForm
from .models import Category, Order, OrderItem, Product # type: ignore

stripe.api_key = settings.STRIPE_SECRET_KEY


def get_cart(request):
    return request.session.setdefault("cart", {})


def get_cart_items(request):
    cart = get_cart(request)
    items = []
    total = Decimal("0.00")

    if not cart:
        return items, total

    product_ids = [int(product_id) for product_id in cart.keys()]
    products = Product.objects.filter(id__in=product_ids)

    for product in products:
        quantity = int(cart.get(str(product.id), 0))
        if quantity <= 0:
            continue
        line_total = product.price * quantity
        items.append({
            "product": product,
            "quantity": quantity,
            "line_total": line_total,
        })
        total += line_total

    return items, total


def home(request):
    featured_products = Product.objects.filter(featured=True)[:4]
    categories = Category.objects.all()
    return render(request, "home.html", {
        "featured_products": featured_products,
        "categories": categories,
    })


def product_list(request):
    category_slug = request.GET.get("category")
    category = None
    products = Product.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    categories = Category.objects.all()
    return render(request, "product_list.html", {
        "products": products,
        "categories": categories,
        "active_category": category,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:3]
    return render(request, "product_detail.html", {
        "product": product,
        "related_products": related_products,
    })


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        cart = get_cart(request)
        quantity = int(request.POST.get("quantity", 1))
        quantity = max(1, quantity)
        cart[str(product.id)] = quantity
        request.session.modified = True
        messages.success(request, f"{product.name} added to your cart.")

    return redirect("product_detail", slug=product.slug)


def cart_view(request):
    items, total = get_cart_items(request)
    return render(request, "cart.html", {
        "items": items,
        "total": total,
    })


def update_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        cart = get_cart(request)
        quantity = int(request.POST.get("quantity", 1))

        if quantity <= 0:
            cart.pop(str(product.id), None)
        else:
            cart[str(product.id)] = quantity

        request.session.modified = True
        messages.info(request, f"{product.name} quantity updated.")

    return redirect("cart")


def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)
    cart.pop(str(product.id), None)
    request.session.modified = True
    messages.warning(request, f"{product.name} removed from your cart.")
    return redirect("cart")


def checkout(request):
    items, total = get_cart_items(request)

    if not items:
        messages.info(request, "Your cart is empty. Add a few products before checking out.")
        return redirect("product_list")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                email=form.cleaned_data["email"],
                phone=form.cleaned_data["phone"],
                address=form.cleaned_data["address"],
                city=form.cleaned_data["city"],
                postal_code=form.cleaned_data["postal_code"],
                country=form.cleaned_data["country"],
                total=total,
            )

            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                    price=item["product"].price,
                )

            line_items = []
            for item in items:
                line_items.append({
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": item["product"].name,
                            "description": item["product"].description[:100],
                        },
                        "unit_amount": int(item["product"].price * 100),
                    },
                    "quantity": item["quantity"],
                })

            try:
                session = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    line_items=line_items,
                    mode="payment",
                    success_url=request.build_absolute_uri(f"/order/{order.id}/success/"),
                    cancel_url=request.build_absolute_uri("/checkout/"),
                    customer_email=order.email,
                )
                order.stripe_session_id = session.id
                order.save()
                request.session["cart"] = {}
                request.session.modified = True
                return redirect(session.url, code=303)
            except Exception as e:
                messages.error(request, f"Payment error: {str(e)}")
                order.delete()
                return redirect("checkout")
    else:
        form = CheckoutForm()

    return render(request, "checkout.html", {
        "form": form,
        "items": items,
        "total": total,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
    })


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = "paid"
    order.save()
    return render(request, "order_success.html", {"order": order})


@login_required
def account_orders(request):
    orders = request.user.orders.all()
    return render(request, "account_orders.html", {"orders": orders})


@login_required
def account_detail(request):
    return render(request, "account_detail.html", {"user": request.user})
