from django.db.models import Q
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import GoodForm, GoodDeleteForm
from webapp.models import Good

class IndexView(ListView):
    model = Good
    context_object_name = "goods"
    template_name = "goods/index.html"
    ordering = ['category', 'description']
    search_fields = ['description__icontains']
    paginate_by = 5
    paginate_orphans = 0

    def get_queryset(self):
        return super().get_queryset().filter(remainder__gt=0)


class CreateGoodView(PermissionRequiredMixin, CreateView):
    model = Good
    form_class = GoodForm
    template_name = "goods/good_create.html"
    permission_required = 'webapp.add_good'

    def get_success_url(self):
        return reverse('webapp:good_view', kwargs={'pk': self.object.pk})

class GoodView(DetailView):
    template_name = 'goods/good_view.html'
    model = Good

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object.category
        context['category'] = category
        return context

class GoodUpdateView(PermissionRequiredMixin, UpdateView):
    form_class = GoodForm
    template_name = "goods/good_update.html"
    model = Good
    permission_required = 'webapp.change_good'


class GoodDeleteView(PermissionRequiredMixin, DeleteView):
    model = Good
    template_name = "goods/good_delete.html"
    success_url = reverse_lazy('main_page')
    permission_required = 'webapp.delete_good'

    def dispatch(self, request, *args, **kwargs):
        if self.request.method == "POST":
            self.object_form = GoodDeleteForm(instance=self.get_object(), data=self.request.POST)
        else:
            self.object_form = GoodDeleteForm()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.object_form
        return context

    def post(self, request, *args, **kwargs):
        if self.object_form.is_valid():
            return super().delete(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)