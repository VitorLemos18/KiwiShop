from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from products.models import Product
from .models import CartItem

class CartView(View):
    def get(self, request):
        cart_id = request.session.session_key
        if not cart_id:
            request.session.create()
            cart_id = request.session.session_key
        
        cart_items = CartItem.objects.filter(cart_id=cart_id)
        total = sum(item.total_price for item in cart_items)
        count = cart_items.count()
        
        return render(request, 'cart/cart.html', {
            'cart_items': cart_items,
            'total': total,
            'count': count
        })

class CartAddView(View):
    @method_decorator(csrf_protect)
    def post(self, request):
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        try:
            product = get_object_or_404(Product, id=product_id)
            if product.stock < quantity:
                return JsonResponse({'error': 'Estoque insuficiente'}, status=400)
                
            cart_id = request.session.session_key
            if not cart_id:
                request.session.create()
                cart_id = request.session.session_key
            
            cart_item, created = CartItem.objects.get_or_create(
                cart_id=cart_id,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                new_qty = cart_item.quantity + quantity
                if new_qty <= product.stock:
                    cart_item.quantity = new_qty
                    cart_item.save()
                else:
                    return JsonResponse({'error': 'Estoque insuficiente'}, status=400)
            
            return JsonResponse({
                'status': 'success',
                'message': f'{product.name} adicionado ao carrinho!',
                'count': CartItem.objects.filter(cart_id=cart_id).count()
            })
        except (ValueError, Product.DoesNotExist):
            return JsonResponse({'error': 'Produto inválido'}, status=400)

# Update e Remove iguais (sem csrf_exempt para AJAX simples)
class CartUpdateView(View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 0))
        
        cart_id = request.session.session_key
        cart_item = get_object_or_404(CartItem, cart_id=cart_id, product_id=product_id)
        
        if quantity == 0:
            cart_item.delete()
            return JsonResponse({'status': 'removed'})
        
        if quantity > cart_item.product.stock:
            return JsonResponse({'error': 'Estoque insuficiente'}, status=400)
        
        cart_item.quantity = quantity
        cart_item.save()
        
        return JsonResponse({
            'status': 'success',
            'total': cart_item.total_price,
            'count': CartItem.objects.filter(cart_id=cart_id).count()
        })

class CartRemoveView(View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        cart_id = request.session.session_key
        
        cart_item = get_object_or_404(CartItem, cart_id=cart_id, product_id=product_id)
        cart_item.delete()
        
        return JsonResponse({'status': 'removed'})
