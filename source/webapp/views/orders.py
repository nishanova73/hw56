from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DeleteView

from webapp.forms import CartForm, OrderForm
from webapp.models import Cart, Good, Order, OrderGood


class CartAddView(CreateView):
    model = Cart
    form_class = CartForm

    def form_valid(self, form):
        good = get_object_or_404(Good, pk=self.kwargs.get("pk"))
        qty = form.cleaned_data.get("qty", 1)
        try:
            cart_good = Cart.objects.get(good=good)
            if cart_good.qty + qty <= good.amount:
                cart_good.qty += qty
                cart_good.save()
        except Cart.DoesNotExist:
            if qty <= good.amount:
                Cart.objects.create(good=good, qty=qty)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next = self.request.GET.get("next")
        if next:
            return next
        return reverse("webapp:main_page")


class CartView(ListView):
    template_name = "orders/basket_view.html"
    context_object_name = "cart"

    def get_queryset(self):
        return Cart.get_with_good()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context["total"] = Cart.get_cart_total()
        context["form"] = OrderForm()
        return context


class CartDeleteView(DeleteView):
    model = Cart
    success_url = reverse_lazy("webapp:cart_view")

    def get(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class CartDeleteOneView(DeleteView):
    model = Cart
    success_url = reverse_lazy("webapp:cart_view")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        self.object.qty -= 1
        if self.object.qty < 1:
            self.object.delete()
        else:
            self.object.save()
        return HttpResponseRedirect(success_url)


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy("webapp:main_page")


    def form_valid(self, form):
        response = super().form_valid(form)
        order = self.object

        cart_goods = Cart.objects.all()
        goods = []
        order_goods = []
        for item in cart_goods:
            good = item.good
            qty = item.qty
            good.amount -= qty
            goods.append(good)
            order_goods = OrderGood(good=good, qty=qty, order=order)
            order_goods.append(order_good)

        OrderGood.objects.bulk_create(order_goods)
        Good.objects.bulk_update(goods, ("remainder",))
        cart_goods.delete()
        return response