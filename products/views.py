from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category, Product, Order, OrderItem, Cart, CartItem


class CategoryView(View):
    def get(self, request):
        categories = Category.objects.all()
        context = {
            'categories': categories
        }
        return render(request, 'products/category.html', context=context)


class ProductsView(View):

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        products = Product.objects.filter(category=category)
        context = {
            'products': products,
            'category': category,
        }
        return render(request, 'products/product_list.html', context=context)


class ProductDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        context = {
            'product': product
        }
        return render(request, 'products/product_detail.html', context=context)


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        return redirect('cart-detail')


class CartDetailView(LoginRequiredMixin, View):
    def get(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = cart.items.all()
        context = {
            'cart': cart,
            'cart_items': cart_items,

        }
        return render(request, 'products/cart_detail.html', context=context)


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        cart_item.delete()
        return redirect('cart-detail')


class CheckoutView(LoginRequiredMixin, View):
    def get(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        context = {
            'cart': cart
        }
        return render(request, 'products/checkout.html', context)

    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        order = Order.objects.create(
            user=request.user,
            phone=request.POST.get('phone'),
            email=request.POST.get('email')
        )
        for item in cart.items.all():
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        cart.items.all().delete()
        return redirect('order-detail', pk=order.id)


class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk, user=request.user)
        context = {
            'order': order
        }
        return render(request, 'products/order_detail.html', context)