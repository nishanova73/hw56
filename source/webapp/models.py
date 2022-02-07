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
    remainder = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return f"{self.remainder} * {self.good}"

    class Meta:
        db_table = 'Basket'
        verbose_name = 'basket'
        verbose_name_plural = 'baskets'


# class Order(models.Model):
#     goods = models.ManyToManyField('webapp.Good', related_name='orders', verbose_name='Orders')
#     username = models.CharField(max_length=20, null=False, blank=False)
#     phone = models.IntegerField(null=False, blank=False)
#     address = models.TextField(max_length=50, null=False, blank=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.username}"
#
#     class Meta:
#         db_table = 'Order'
#         verbose_name = 'order'
#         verbose_name_plural = 'orders'