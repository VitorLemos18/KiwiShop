from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),                    # /cart/
    path('add/', views.CartAddView.as_view(), name='add'),             # /cart/add/
    path('update/', views.CartUpdateView.as_view(), name='update'),    # /cart/update/
    path('remove/', views.CartRemoveView.as_view(), name='remove'),    # /cart/remove/
]
