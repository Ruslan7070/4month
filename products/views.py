# Create your views here.
from django.shortcuts import render, redirect
from products.models import *
from products.forms import ProductCreateForms, ReviewCreateForm
from users.utils import get_user_from_request
from django.views.generic import ListView, CreateView

PAGINATION_LIMIT = 4


def main(request):
    if request.method == 'GET':
        products = Product.objects.all()

        data = {
            'products': products,
            'user': get_user_from_request(request)
        }
        return render(request, 'layouts/main.html', context=data)


def products_view(request):
    if request.method == 'GET':
        category_id = request.GET.get('category_id')
        search_text = request.GET.get('search')
        page = int(request.GET.get('page', 1))
        if category_id:
            products = Product.objects.filter(category_id=category_id)
        else:
            products = Product.objects.all()

        if search_text:
            products = products.filter(title__icontains=search_text)
        max_page = round(products.__len__() / PAGINATION_LIMIT)
        products = products[PAGINATION_LIMIT * (page - 1): PAGINATION_LIMIT * page]
        data = {
            'products': products,
            'user': get_user_from_request(request),
            'category_id': category_id,
            'max_page': range(1, max_page + 1)
        }

        return render(request, 'products/products.html', context=data)


def detail_view(request, **kwargs):
    if request.method == 'GET':
        product = Product.objects.get(id=kwargs['id'])
        reviews = Review.objects.filter(product=product)

        data = {
            'product': product,
            'reviews': reviews,
            'form': ReviewCreateForm,
            'user': get_user_from_request(request)
        }

        return render(request, 'products/detail.html', context=data)
    if request.method == 'POST':
        form = ReviewCreateForm(data=request.POST)
        if form.is_valid():
            Review.objects.create(
                author=1,
                text=form.cleaned_data.get('text'),
                product_id=kwargs['id']
            )
            return redirect(f"/product/{kwargs['id']}/")


class CategoriesView(ListView):
    model = Category
    template_name = "categories/categories.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {
            'object_list': self.get_queryset(),
            'user': get_user_from_request(self.request)
        }
        return context


def products_create_view(request):
    if request.method == 'GET':
        data = {
            'form': ProductCreateForms,
            'user': get_user_from_request(request)
        }
        return render(request, 'products/create.html', context=data)

    if request.method == "POST":
        form = ProductCreateForms(data=request.POST)

        if form.is_valid():
            Product.objects.create(
                author_id=1,
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                price=form.cleaned_data.get('price'),
                rate=form.cleaned_data.get('rate'),
                category_id=form.cleaned_data.get('category')
            )
            return redirect('/products')
        else:
            data = {
                'form': form,
                'user': get_user_from_request(request)
            }
            return render(request, 'products/create.html', context=data)


class ProductsCreateView(ListView, CreateView):
    model = Product
    template_name = 'products/create.html'
    form_class = ProductCreateForms

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'form': kwargs['form'] if kwargs.get('form') else self.form_class,
            'user': get_user_from_request(self.request)
        }

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            self.model.objects.create(
                author_id=1,
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                price=form.cleaned_data.get('price'),
                rate=form.cleaned_data.get('rate'),
                category_id=form.cleaned_data.get('category')
            )
            return redirect('/products')
        else:

            return render(request, self.template_name, context=self.get_context_data(form=form))
