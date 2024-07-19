from django.db import models
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    # image = models.ImageField(upload_to='media/category_images/')

    class Meta:
        db_table = 'categories'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='media/images/')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    made_in = models.CharField(max_length=100)

    class Meta:
        db_table = 'products'
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('S', 'Shipped'),
        ('D', 'Delivered'),
        ('C', 'Cancelled'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orders'
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey('Order', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'order_items'
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_total_price(self):
        return sum(item.get_total_price for item in self.items.all())

    class Meta:
        db_table = 'carts'
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey('Cart', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def get_total_price(self):
        return self.product.price * self.quantity

    class Meta:
        db_table = 'cart_items'
        verbose_name = _('Cart Item')
        verbose_name_plural = _('Cart Items')

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
