from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

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

    def get_absolute_url(self):
        return reverse('good_view', kwargs={'pk': self.pk})

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


class Basket(models.Model):
    good = models.ForeignKey("webapp.Good", on_delete=models.CASCADE,
                                 related_name="good",
                                 verbose_name="Good",
                                 )
    remainder = models.PositiveIntegerField( default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.remainder} * {self.good}"

    class Meta:
        db_table = 'Basket'
        verbose_name = 'basket'
        verbose_name_plural = 'baskets'


class Order(models.Model):
    name = models.CharField(max_length=10, verbose_name='Name')
    phone = models.CharField(max_length=10, verbose_name='Phone')
    address = models.CharField(max_length=50, verbose_name='Address')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    goods = models.ManyToManyField('webapp.Good', related_name='orders', verbose_name='Goods',
                                      through='webapp.OrderGood', through_fields=['order', 'good'])

    def __str__(self):
        return f'{self.name} : {self.phone}'

    class Meta:
        db_table = 'Order'
        verbose_name = 'order'
        verbose_name_plural = 'orders'


class OrderGood(models.Model):
    good = models.ForeignKey('webapp.Good', on_delete=models.CASCADE,
                                verbose_name='Good', related_name='order_goods')
    order = models.ForeignKey('webapp.Order', on_delete=models.CASCADE,
                              verbose_name='Order', related_name='order_goods')
    remainder = models.PositiveIntegerField(verbose_name='Quantity')

    def __str__(self):
        return f'{self.good.description} - {self.order.name}'

    class Meta:
        db_table = 'OrderGood'
        verbose_name = 'Good in order'
        verbose_name_plural = 'Goods in order'