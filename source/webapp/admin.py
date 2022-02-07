from django.contrib import admin

# Register your models here.
from webapp.models import Good, Category, Basket, Order, OrderGood

class GoodAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'detailed_description', 'category', 'remainder', 'price']
    list_filter = ['category']
    search_fields = ['description', 'category']
    fields = ['description', 'detailed_description', 'category', 'remainder', 'price']
    readonly_fields = []


class OrderGoodAdmin(admin.TabularInline):
    model = OrderGood
    fields = ('good', 'remainder')
    extra = 0



class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'phone', 'created_at')
    list_display_links = ('pk', 'name')
    ordering = ('-created_at',)
    inlines = (OrdergoodAdmin,)


admin.site.register(Good, GoodAdmin)
admin.site.register(Category)
admin.site.register(Basket)
admin.site.register(Order, OrderAdmin)
