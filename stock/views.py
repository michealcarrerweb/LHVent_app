from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView, 
    UpdateView, 
    DeleteView, 
    FormView
)
from .forms import (
    BaseForm, 
    ProductUpdateForm, 
    ProductCreateForm, 
    ItemAddDamagedForm, 
    ImageUpdateForm, 
    ItemAddedForm
)
from .models import Base, Product
from company.models import Company
from source_utils.permission_mixins import (
    SuperUserCheckMixin, 
    ManagerCheckMixin,
    WarehouseAndManagerCheckMixin
)
from source_utils.view_mixins import DeleteViewMixin


class BaseAuthMixin(WarehouseAndManagerCheckMixin):
    model = Base


class BaseTypeList(BaseAuthMixin, ListView):
    template_name = "product/base_list.html"
    title = "Product Category Options"


class BaseSuccessMixin(BaseAuthMixin, SuccessMessageMixin):
    template_name = "form.html"
    form_class = BaseForm
    success_url = reverse_lazy('product:base_product_list')

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            base=self.object.category,
        )


class BaseTypeCreate(BaseSuccessMixin, CreateView):
    success_message = "%(base)s was successfully created"
    title = "New Product Category"


class BaseTypeUpdate(BaseSuccessMixin, UpdateView):
    success_message = "%(base)s was successfully updated"
    title = "Update Product Category"
    url_insert = "product:base_product_delete"


class BaseTypeDelete(DeleteViewMixin):
    model = Base
    success_url = reverse_lazy('product:base_product_list')


class ItemAuthMixin(BaseAuthMixin):
    model = Product


class ItemList(ItemAuthMixin, ListView):
    template_name = "product/item_list.html"
    title = "All Products"


class ItemDetail(ItemAuthMixin, DetailView):
    template_name = "product/item_detail.html"


class ItemMessageMixin(ItemAuthMixin, SuccessMessageMixin):
    template_name = "form.html"
    success_url = reverse_lazy('product:item_list')
    form_class = ProductCreateForm

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            item=self.object.item,
        )


class ItemCreate(ItemMessageMixin, CreateView):
    success_message = "%(item)s was successfully created"
    title = "New Product"


class BaseItemCreate(ItemCreate):

    def get_initial(self):
        base = get_object_or_404(Base, slug=self.args[0])
        return {
            'base':base
        }


class SupplierItemCreate(ItemCreate):

    def get_initial(self):
        supplier = get_object_or_404(Company, slug=self.args[0])
        return {
            'supplier':supplier
        }


class ItemUpdate(ItemMessageMixin, UpdateView):
    success_message = "%(item)s was successfully updated"
    url_insert = "product:item_delete"

    def get_context_data(self, **kwargs):
        context = super(ItemUpdate, self).get_context_data(**kwargs)
        context['title'] = "Update {}".format(
            self.object)
        return context


class ItemAddDamaged(ItemMessageMixin, FormView):
    success_message = "%(quantity)s damaged was successfully altered for %(item)s"
    form_class = ItemAddDamagedForm

    def get_item(self):
        return get_object_or_404(Product, slug=self.args[0])

    def form_valid(self, form):
        units_damaged = form.cleaned_data["damaged_or_lost"]
        item = self.get_item()
        item.units_damaged_or_lost += units_damaged
        item.quantity -= units_damaged
        item.save()
        return super(ItemAddDamaged, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ItemAddDamaged, self).get_context_data(**kwargs)
        item = self.get_item()
        context['title'] = "Add Damaged or Lost to {}?".format(
            item.__str__())
        return context

    def get_success_message(self, cleaned_data):
        item = self.get_item()
        return self.success_message % dict(
            cleaned_data,
            quantity=cleaned_data['damaged_or_lost'],
            item=item.__str__()
        )


class ItemAdd(ItemMessageMixin, FormView):
    success_message = "%(quantity)s additional was successfully added for %(item)s"
    form_class = ItemAddedForm

    def get_item(self):
        return get_object_or_404(Product, slug=self.args[0])

    def form_valid(self, form):
        added = form.cleaned_data["added"]
        item = self.get_item()
        item.quantity += added
        item.save()
        return super(ItemAdd, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ItemAdd, self).get_context_data(**kwargs)
        item = self.get_item()
        context['title'] = "Add to {}?".format(
            item.__str__())
        return context

    def get_success_message(self, cleaned_data):
        item = self.get_item()
        return self.success_message % dict(
            cleaned_data,
            quantity=cleaned_data['added'],
            item=item.__str__()
        )


class ItemCategoryList(ItemAuthMixin, ListView):
    template_name = "product/item_list.html"

    def get_queryset(self):
        self.category = get_object_or_404(Base, slug=self.args[0])
        return Product.objects.filter(base=self.category)

    def get_context_data(self, **kwargs):
        context = super(ItemCategoryList, self).get_context_data(**kwargs)
        context['title'] = "Products in {}". format(self.category)
        return context


class ItemSupplierList(ItemAuthMixin, ListView):
    template_name = "product/item_list.html"

    def get_queryset(self):
        self.company = get_object_or_404(Company, slug=self.args[0])
        return Product.objects.filter(supplier=self.company)

    def get_context_data(self, **kwargs):
        context = super(ItemSupplierList, self).get_context_data(**kwargs)
        context['title'] = "Products from {}". format(self.company)
        return context


class ItemDelete(DeleteViewMixin):
    model = Product
    success_url = reverse_lazy('product:item_list')


class ImageUpdate(ItemMessageMixin, UpdateView):
    success_message = "%(item)s was successfully updated"
    form_class = ImageUpdateForm
    title = "Update Image"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            item=self.object.item + " image"
        )


class ImageDetail(ItemAuthMixin, DetailView):
    template_name = "product/image_detail.html"