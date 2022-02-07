from django.urls import path
from django.views.generic import RedirectView
from webapp.views import(
                        IndexView,
                        CreateGoodView,
                        GoodView,
                        GoodUpdateView,
                        GoodDeleteView,
                        BasketView,
                        BasketAddView,
                        BasketDeleteView,
                        BasketDeleteOneView,
                        OrderCreateView,
                        )



urlpatterns = [
    path('', IndexView.as_view(), name="main_page"),
    path('goods/', RedirectView.as_view(pattern_name="main_page")),
    path('good/create_good/', CreateGoodView.as_view(), name="good_add"),
    path('good_view/<int:pk>/', GoodView.as_view(template_name="goods/good_view.html"), name="good_view"),
    path('good_view/<int:pk>/update/', GoodUpdateView.as_view(), name="good_update"),
    path('good_view/<int:pk>/delete/', GoodDeleteView.as_view(), name="good_delete"),
    path('basket/<int:pk>/delete/', BasketDeleteView.as_view(), name='basket_delete'),
    path('basket/<int:pk>/delete/one/', BasketDeleteOneView.as_view(), name='basket_delete_one'),
    path('order/create/', OrderCreateView.as_view(), name='order_create'),
    path('basket/<int:pk>/', BasketView.as_view(), name='basket_view'),
]