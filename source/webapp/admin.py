from django.contrib import admin

# Register your models here.
from webapp.models import Good, Cart, Order, OrderGood


class GoodAdmin(admin.ModelAdmin):
    list_display = ('pk', 'description', 'detailed_description', 'category', 'remainder', 'price')
    list_display_links = ('pk', 'description')
    list_filter = ('category',)
    search_fields = ('description',)


class OrderGoodInline(admin.TabularInline):
    model = OrderGood
    fields = ('good', 'qty')
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'phone', 'created_at')
    list_display_links = ('pk', 'name')
    ordering = ["-created_at"]
    inlines = (OrderGoodInline,)


admin.site.register(Good, GoodAdmin)
admin.site.register(Cart)
admin.site.register(Order, OrderAdmin)
