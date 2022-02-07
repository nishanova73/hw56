from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView

from webapp.forms import BasketAddForm, OrderForm
from webapp.models import Basket, Good, Order, OrderGood


class BasketView(DetailView):
    template_name = 'orders/create.html'
    context_object_name = 'basket'

    def get_queryset(self):
        return Basket.get_with_good().filter(pk__in=self.get_basket_ids())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['basket_total'] = Basket.get_basket_total(ids=self.get_basket_ids())
        context['form'] = OrderForm()
        return context

    def get_basket_ids(self):
        basket_ids = self.request.session.get('basket_ids', [])
        return self.request.session.get('basket_ids', [])


class BasketAddView(CreateView):
    model = Basket
    form_class = BasketAddForm

    def post(self, request, *args, **kwargs):
        self.good = get_object_or_404(Good, pk=self.kwargs.get('pk'))
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        remainder = form.cleaned_data.get('remainder', 1)

        try:
            basket_good = Basket.objects.get(product=self.good, pk__in=self.get_basket_ids())
            basket_good.remainder += remainder
            if basket_good.remainder <= self.good.amount:
                basket_good.save()
        except Basket.DoesNotExist:
            if remainder <= self.good.amount:
                basket_good = Basket.objects.create(good=self.good, remainder=remainder)
                self.save_to_session(basket_good)

        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return redirect(self.get_success_url())

    def get_success_url(self):
        next = self.request.GET.get('next')
        if next:
            return next
        return reverse('main_page')

    def get_basket_ids(self):
        return self.request.session.get('basket_ids', [])

    def save_to_session(self, basket_good):
        basket_ids = self.request.session.get('basket_ids', [])
        if basket_good.pk not in basket_ids:
            basket_ids.append(basket_good.pk)
        self.request.session['basket_ids'] = basket_ids


class BasketDeleteView(DeleteView):
    model = Basket
    success_url = reverse_lazy('basket_view')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.delete_from_session()
        self.object.delete()
        return redirect(success_url)

    def delete_from_session(self):
        basket_ids = self.request.session.get('basket_ids', [])
        basket_ids.remove(self.object.pk)
        self.request.session['basket_ids'] = basket_ids

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class BasketDeleteOneView(BasketDeleteView):
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.remainder -= 1
        if self.object.remainder < 1:
            self.delete_from_session()
            self.object.delete()
        else:
            self.object.save()

        return redirect(success_url)


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('main_page')

    def form_valid(self, form):
        response = super().form_valid(form)
        order = self.object
        basket_goods = Basket.objects.all()
        goods = []
        order_goods = []
        for item in basket_goods:
            good = item.good
            remainder = item.remainder
            good.amount -= remainder
            goods.append(good)
            order_good = OrderGood(order=order, good=good, remainder=remainder)
            order_goods.append(order_good)
        OrderGood.objects.bulk_create(order_goods)
        Good.objects.bulk_update(goods, ('remainder',))
        basket_goods.delete()
        return response

    def form_invalid(self, form):
        return redirect('basket_view')