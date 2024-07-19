from django.urls import path
from .views import *

urlpatterns = [
    path('category/', CategoryView.as_view(), name='category-list'),
    path('product_list/<int:pk>/', ProductsView.as_view(), name='product-list'),
    path('product_detail/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('cart/add/<int:pk>/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/remove/<int:product_id>/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('cart/detail/', CartDetailView.as_view(), name='cart-detail'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order-detail')
]
