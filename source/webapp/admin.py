from django.contrib import admin

# Register your models here.
from webapp.models import Good, Category, Basket

class GoodAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'detailed_description', 'category', 'remainder', 'price']
    list_filter = ['category']
    search_fields = ['description', 'category']
    fields = ['description', 'detailed_description', 'category', 'remainder', 'price']
    readonly_fields = []

admin.site.register(Good, GoodAdmin)
admin.site.register(Category)
admin.site.register(Basket)