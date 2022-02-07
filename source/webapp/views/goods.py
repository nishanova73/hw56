from django.db.models import Q
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import GoodForm, SearchForm, GoodDeleteForm
from webapp.models import Good

class IndexView(ListView):
    model = Good
    context_object_name = "goods"
    template_name = "goods/index.html"
    paginate_by = 5
    paginate_orphans = 0

    def get(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)


    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            print(self.search_value)
            query = Q(description__icontains=self.search_value) | Q(detailed_description__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset.order_by("-description").reverse().order_by("category").reverse()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = SearchForm()
        if self.search_value:
            context['form'] = SearchForm(initial={"search": self.search_value})
            context['search'] = self.search_value
        return context

    def get_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")


class CreateGoodView(CreateView):
    model = Good
    form_class = GoodForm
    template_name = "goods/good_create.html"


class GoodView(DetailView):
    template_name = 'goods/good_view.html'
    model = Good

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object.category
        context['category'] = category
        return context

class GoodUpdateView(UpdateView):
    form_class = GoodForm
    template_name = "goods/good_update.html"
    model = Good


class GoodDeleteView(DeleteView):
    model = Good
    template_name = "goods/good_delete.html"
    success_url = reverse_lazy('main_page')

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