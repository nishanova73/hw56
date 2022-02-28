from django.urls import path

from webapp.views import (
                            IndexView,
                            CreateGoodView,
                            GoodView,
                            GoodUpdateView,
                            GoodDeleteView,
                            CartAddView,
                            CartView,
                            CartDeleteView,
                            CartDeleteOneView,
                            OrderCreateView,
                          )

app_name = "webapp"

urlpatterns = [
    path('', IndexView.as_view(), name='main_page'),
    path('product/<int:pk>/', GoodView.as_view(), name='good_view'),
    path('products/add/', CreateGoodView.as_view(), name='good_create'),
    path('product/<int:pk>/update/', GoodUpdateView.as_view(), name='good_update'),
    path('product/<int:pk>/delete/', GoodDeleteView.as_view(), name='good_delete'),
    path('product/<int:pk>/add-to-cart/', CartAddView.as_view(), name='good_add_to_cart'),
    path('cart/', CartView.as_view(), name='cart_view'),
    path('cart/<int:pk>/delete/', CartDeleteView.as_view(), name='cart_delete_view'),
    path('cart/<int:pk>/delete-one/', CartDeleteOneView.as_view(), name='cart_delete_one_view'),
    path('order/create/', OrderCreateView.as_view(), name='order_create_view'),
]