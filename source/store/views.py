from copy import deepcopy
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic import DeleteView, DetailView, ListView, CreateView, UpdateView

from .form import ProductForm, SearchForm
from .models import Product, Order


class StatMixin:
    request = None

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.set_common_stat()
        self.set_page_time()
        return super().dispatch(request, *args, **kwargs)

    def set_common_stat(self):
        if 'stat' not in self.request.session:
            self.request.session['stat'] = {}
        stat = self.request.session.get('stat', {})
        if 'common_start_time' not in stat:
            stat['common_start_time'] = datetime.now().strftime('%d/%m/%y %H:%M:%S')
        self.request.session['stat'] = stat

    def set_page_time(self):
        if 'stat' not in self.request.session:
            self.request.session['stat'] = {}
        stat = self.request.session.get('stat', {})
        if 'page' not in stat.keys():
            stat['page'] = {}
        page = stat['page']
        if self.request.path not in page:
            page[self.request.path] = {}
            page[self.request.path]['time'] = 0
        if 'new' in stat:
            old_time = page[stat['new']['path']]['time']
            time = (datetime.now() - datetime.strptime(stat['new']['start'], '%d/%m/%y %H:%M:%S')).seconds
            new_time = int(old_time) + time
            page[stat['new']['path']]['time'] = new_time
        else:
            stat['new'] = {}
        stat['new']['start'] = datetime.now().strftime('%d/%m/%y %H:%M:%S')
        stat['new']['path'] = self.request.path
        stat['page'] = page
        self.request.session['stat'] = stat


class StatView(StatMixin, View):
    def get(self, request, *args, **kwargs):
        common_time = 0
        if 'stat' not in self.request.session:
            self.request.session['stat'] = {}
        stat = self.request.session.get('stat', {})
        stat = deepcopy(stat)

        if 'common_start_time' in stat:
            start = datetime.strptime(stat['common_start_time'], '%d/%m/%y %H:%M:%S')
            end = datetime.now()
            common_time = str(end - start)

        if 'page' not in stat:
            stat['page'] = {}
        pages = stat['page']
        for key, values in pages.items():
            pages[key]['time'] = datetime.fromtimestamp(int(pages[key]['time'])).strftime("%H:%M:%S")
        if '/stat/' in pages:
            pages.pop('/stat/')
        return render(request, 'stat.html', context={'time': common_time, 'pages': pages})


class ProductIndexView(StatMixin, ListView):
    model = Product
    template_name = 'products/index.html'
    context_object_name = 'products'
    paginate_by = 8
    paginate_orphans = 0

    def get(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(title__icontains=self.search_value) | Q(category__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset.filter(residue__gt=0).order_by('category', 'title')

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
            return self.form.cleaned_data.get('search')


class ProductDetailView(StatMixin, DetailView):
    model = Product
    template_name = 'products/view.html'


class ProductCreateView(PermissionRequiredMixin, StatMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/create.html"
    permission_required = 'webapp.add_product'

    def get_success_url(self):
        return reverse('store:product_view', kwargs={'pk': self.object.pk})


class ProductUpdateView(PermissionRequiredMixin, StatMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "products/update.html"
    permission_required = 'webapp.change_product'

    def get_success_url(self):
        return reverse('store:product_view', kwargs={'pk': self.object.pk})


class ProductDeleteView(PermissionRequiredMixin, StatMixin, DeleteView):
    model = Product
    template_name = 'products/delete.html'
    permission_required = 'webapp.delete_product'

    def get_success_url(self):
        return reverse('store:product_index')


class CartIndexView(StatMixin, ListView):
    template_name = 'cart/index.html'

    def get_queryset(self):
        pass

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        products = self.request.session.get('products', {})
        prods_in_basket = []
        total = 0
        for key, value in products.items():
            product = Product.objects.get(id=int(key))
            unit_total = product.price * value
            total += unit_total
            prods_in_basket.append({'prod': product, 'quantity': value, 'unit_total': unit_total})
        context['prods'] = prods_in_basket
        context['total'] = total
        return context


class CartAddView(StatMixin, View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs.get('pk'))
        if product.residue > 0:
            if not request.session.get('products'):
                request.session['products'] = {}
            products = request.session.get('products')
            messages.success(self.request, f'Добавлен товар :{product.title} ')
            if str(product.id) not in products.keys():
                products[str(product.id)] = 1
            else:
                products[str(product.id)] += 1
            request.session['products'] = products
            return redirect(request.META.get('HTTP_REFERER'))


class CartDeleteView(StatMixin, View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs.get('pk'))
        product_pk = kwargs['pk']
        products = request.session.get('products', {})
        messages.warning(self.request, f'Удален 1 товар: "{product.title}"')
        products[str(product_pk)] -= 1
        if products[str(product_pk)] <= 0:
            products.pop(str(product_pk))
            messages.warning(self.request, f'Товар "{product.title}" удален')
        request.session['products'] = products
        return redirect('store:cart_view')


class MakeOrderView(StatMixin, View):
    def post(self, request, *args, **kwargs):
        products = request.session.get('products', {})
        print(products)
        product_ids = products.keys()
        new_products = Product.objects.filter(id__in=product_ids)
        for product in new_products:
            order = Order()
            if request.user.is_authenticated:
                order.user = request.user
            else:
                order.user = None
            order.product = product
            for k, v in products.items():
                if k == str(product.id):
                    order.quantity = v
                    product.residue = product.residue - v
                    product.save()
            order.save()
        products = {}
        request.session['products'] = products
        messages.success(self.request, f'Заказ успешно оформлен!')
        return redirect('store:product_index')


class OrdersView(StatMixin, ListView):
    template_name = 'order/orders.html'
    model = Order
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = self.request.user.order.all().order_by('-create_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Order.objects.filter(user_id=self.request.user.id)
        context['product'] = product
        return context
