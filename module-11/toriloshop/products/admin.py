from django.contrib import admin
from .models import Category, Product

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


def mark_as_out_of_stock(modeladmin, request, queryset):
    """Custom admin action: Mark products as out of stock."""
    updated = queryset.update(stock=0, is_available=False)
    modeladmin.message_user(request, f'{updated} product(s) marked as out of stock.')
mark_as_out_of_stock.short_description = 'Mark as out of stock'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'stock', 'is_available')
    list_filter = ('category', 'is_available', 'created_at')
    search_fields = ('name', 'category__name')
    ordering = ('-created_at',)
    fields = ('name', 'price', 'stock', 'category', 'image', 'is_available')
    actions = [mark_as_out_of_stock]
