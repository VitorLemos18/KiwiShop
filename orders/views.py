from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib import messages
from django.http import JsonResponse
from cart.models import CartItem
from products.models import Product
from .models import Order, OrderItem
from .forms import CheckoutForm

class CheckoutView(View):
    def get(self, request):
        cart_id = request.session.session_key
        if not cart_id:
            request.session.create()
            cart_id = request.session.session_key
        
        cart_items = CartItem.objects.filter(cart_id=cart_id)
        if not cart_items.exists():
            messages.warning(request, 'Seu carrinho está vazio!')
            return redirect('cart:cart')
        
        total = sum(item.total_price for item in cart_items)
        form = CheckoutForm()
        
        return render(request, 'orders/checkout.html', {
            'cart_items': cart_items,
            'total': total,
            'form': form
        })
    
    def post(self, request):
        cart_id = request.session.session_key
        cart_items = CartItem.objects.filter(cart_id=cart_id)
        
        if not cart_items.exists():
            return redirect('cart:cart')
        
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Criar pedido
            order = Order.objects.create(
                session_id=cart_id,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                zip_code=form.cleaned_data['zip_code'],
                total=sum(item.total_price for item in cart_items)
            )
            
            # Criar itens do pedido
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )
            
            # Limpar carrinho
            cart_items.delete()
            
            messages.success(request, f'Pedido #{order.order_number} criado com sucesso!')
            return redirect('orders:success', order_number=order.order_number)
        
        total = sum(item.total_price for item in cart_items)
        return render(request, 'orders/checkout.html', {
            'cart_items': cart_items,
            'total': total,
            'form': form
        })

class OrderSuccessView(View):
    def get(self, request, order_number):
        order = get_object_or_404(Order, order_number=order_number)
        return render(request, 'orders/success.html', {'order': order})

class OrderListView(View):
    def get(self, request):
        orders = Order.objects.filter(session_id=request.session.session_key).order_by('-created')
        return render(request, 'orders/list.html', {'orders': orders})
