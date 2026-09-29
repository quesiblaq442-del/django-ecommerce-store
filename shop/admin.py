from django.contrib import admin
from .models import Category, Order, OrderItem, Product, Review, Wishlist


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    fields = ("name", "price", "stock", "featured")
    readonly_fields = ("created_at",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "product_count")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductInline]

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = "Products"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "featured", "average_rating", "review_count")
    list_filter = ("category", "featured", "created_at")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at", "average_rating", "review_count")
    fieldsets = (
        ("Basic Information", {"fields": ("name", "slug", "category", "description")}),
        ("Pricing & Inventory", {"fields": ("price", "stock")}),
        ("Display", {"fields": ("image", "featured")}),
        ("Ratings", {"fields": ("average_rating", "review_count")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    def average_rating(self, obj):
        rating = obj.average_rating()
        if rating > 0:
            return f"{rating:.1f}/5.0 ⭐"
        return "No ratings"
    average_rating.short_description = "Average Rating"

    def review_count(self, obj):
        return obj.review_count()
    review_count.short_description = "Reviews"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user_email", "rating", "title", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("product__name", "user__email", "title", "comment")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Review Details", {"fields": ("product", "user", "rating", "title", "comment")}),
        ("Engagement", {"fields": ("helpful_count",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = "User"


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("user_email", "product_count", "updated_at")
    search_fields = ("user__email",)
    readonly_fields = ("created_at", "updated_at")
    filter_horizontal = ("products",)

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = "User"

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = "Products"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "price")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "user_email", "total", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("id", "user__email", "email", "first_name", "last_name")
    readonly_fields = ("stripe_session_id", "created_at", "updated_at")
    inlines = [OrderItemInline]
    fieldsets = (
        ("Order Information", {"fields": ("id", "user", "status")}),
        ("Customer Details", {"fields": ("first_name", "last_name", "email", "phone")}),
        ("Shipping Address", {"fields": ("address", "city", "postal_code", "country")}),
        ("Payment", {"fields": ("total", "stripe_session_id")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    def order_number(self, obj):
        return f"#{obj.id}"
    order_number.short_description = "Order #"

    def user_email(self, obj):
        return obj.user.email if obj.user else obj.email
    user_email.short_description = "Customer"

    actions = ["mark_as_shipped", "mark_as_delivered"]

    def mark_as_shipped(self, request, queryset):
        updated = queryset.update(status="shipped")
        self.message_user(request, f"{updated} orders marked as shipped.")
    mark_as_shipped.short_description = "Mark selected orders as shipped"

    def mark_as_delivered(self, request, queryset):
        updated = queryset.update(status="delivered")
        self.message_user(request, f"{updated} orders marked as delivered.")
    mark_as_delivered.short_description = "Mark selected orders as delivered"
