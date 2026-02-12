from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Homepage / Catálogo
    path('', views.ProductListView.as_view(), name='product_list'),
    
    # Detalhes Produto: /smartwatch-kiwi-x1/
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]
