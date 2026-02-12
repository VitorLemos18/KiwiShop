from django.contrib import admin
from .models import CartItem

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'cart_id', 'created', 'updated']
    list_filter = ['created', 'updated']
    search_fields = ['cart_id', 'product__name']
    readonly_fields = ['created', 'updated']
    
    fieldsets = (
        ('Informações do Item', {
            'fields': ('product', 'quantity', 'cart_id')
        }),
        ('Timestamps', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product')
