from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import F, ExpressionWrapper as E, Sum

# Create your models here.


class Good(models.Model):
    description = models.CharField(max_length=100, null=False, blank=False, verbose_name='description')
    detailed_description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='detailed_description')
    category = models.ForeignKey("webapp.Category", on_delete=models.CASCADE,
                             related_name="categories",
                             verbose_name="Category",
                             )
    remainder = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"{self.pk}. {self.description}: {self.category}"

    class Meta:
        db_table = 'Goods'
        verbose_name = 'good'
        verbose_name_plural = 'goods'


class Category(models.Model):
    text = models.CharField(max_length=15, default='other', null=False)

    def __str__(self):
        return f"{self.text}"

    class Meta:
        db_table = 'Categories'
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Cart(models.Model):
    good = models.ForeignKey('webapp.Good', on_delete=models.CASCADE,
                                verbose_name='Good', related_name='in_cart')
    qty = models.PositiveIntegerField(verbose_name='Quantity', default=1)

    def __str__(self):
        return f'{self.good.description} - {self.qty}'

    @classmethod
    def get_with_total(cls):
        return cls.objects.annotate(total=E(F("qty") * F("good__price"), output_field=models.DecimalField()))

    @classmethod
    def get_with_good(cls):
        return cls.get_with_total().select_related("good")

    @classmethod
    def get_cart_total(cls):
        total = cls.get_with_total().aggregate(cart_total=Sum("total"))
        return total['cart_total']

    class Meta:
        verbose_name = 'Good in order'
        verbose_name_plural = 'Goods in order'


class Order(models.Model):
    name = models.CharField(max_length=50, verbose_name='Name')
    phone = models.CharField(max_length=30, verbose_name='Phone')
    address = models.CharField(max_length=100, verbose_name='Address')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    products = models.ManyToManyField('webapp.Good', related_name='orders', verbose_name='Orders',
                                      through='webapp.OrderGood', through_fields=['order', 'good'])

    def __str__(self):
        return f'{self.name} - {self.phone}'

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderGood(models.Model):
    good = models.ForeignKey('webapp.Good', on_delete=models.CASCADE,
                                verbose_name='order', related_name='order_goods')
    order = models.ForeignKey('webapp.Order', on_delete=models.CASCADE,
                              verbose_name='order', related_name='order_goods')
    qty = models.PositiveIntegerField(verbose_name='Quantity')

    def __str__(self):
        return f'{self.good.description} - {self.order.name}'

    class Meta:
        verbose_name = 'Good in order'
        verbose_name_plural = 'Goods in order'