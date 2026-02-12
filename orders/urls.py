from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('success/<str:order_number>/', views.OrderSuccessView.as_view(), name='success'),
    path('meus-pedidos/', views.OrderListView.as_view(), name='list'),
]
