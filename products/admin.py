from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Category, Product

class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    fields = ['name', 'price', 'stock', 'is_active']
    readonly_fields = ['created_at']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductInline]
    
    def product_count(self, obj):
        count = obj.product_count()
        url = reverse('admin:products_product_changelist') + f'?category__id__exact={obj.id}'
        return format_html('<a href="{}">{}</a>', url, count)
    product_count.short_description = 'Produtos'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_active', 'image_preview', 'featured']
    list_filter = ['category', 'is_active', 'featured', 'created_at']
    search_fields = ['name', 'description', 'sku']
    list_editable = ['price', 'stock', 'is_active', 'featured']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'category', 'slug', 'sku')
        }),
        ('Preço e Estoque', {
            'fields': ('price', 'stock', 'is_active', 'featured')
        }),
        ('Descrição', {
            'fields': ('description', 'short_description')
        }),
        ('Imagem', {
            'fields': ('image',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:60px; height:60px; object-fit:cover;"/>',
                obj.image_url
            )
        return "Sem imagem"
    image_preview.short_description = "Imagem"
