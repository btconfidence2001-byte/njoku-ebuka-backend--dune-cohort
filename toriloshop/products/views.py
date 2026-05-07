from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm, CategoryForm
from .models import Product, Category
from django.db.models import Count
from django.contrib import messages

# Create your views here.

def home(request):
    """Home page view"""
    # You can show featured products or just a simple home page
    featured_products = Product.objects.all()[:3] # Show first 3 products
    context = {'featured_products': featured_products}
    return render(request, 'products/home.html', context)

def about (request):
    """About page view"""
    return render(request, 'products/about.html')

def product_list(request):
    """Display all products"""
    # Fetch all products from the database
    products = Product.objects.all()
    # The context dict maps variable names to values available in the templatpye
    context = {'products': products}
    return render(request, 'products/product_list.html', context)


def product_detail(request, pk):
    """Display a single product detail"""
    # pk is captured from the URL - e.g. /products/3/ gives pk=3
    # get_object_or_404 returns the product or shows a 404 page automatically
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'products/product_detail.html', context)

def category_list(request):
    """Display all categories with product counts"""
    # annotate() adds a computed field to each object in the QuerySet
    # product_count is the number of products linked to each category
    categories = Category.objects.annotate(product_count=Count('products'))
    context = {'categories': categories}
    return render(request, 'products/category_list.html', context)



@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()

    return render(request, 'products/add_product.html', {'form': form})

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/edit_product.html', {
        'form': form,
        'product': product,
    })

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this product.')
        return redirect('product_list')

    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'{product_name} deleted successfully.')
        return redirect('product_list')

    return render(request, 'products/delete_product.html', {
        'product': product,
    })

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()

    return render(request, 'products/add_category.html', {
        'form': form,
    })

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()
    return render(request, 'products/category_products.html', {
        'category': category,
        'products': products,
    })

@login_required
def edit_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'products/edit_category.html', {
        'form': form,
        'category': category,
    })

@login_required
def delete_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    product_count = category.products.count()

    if request.method == 'POST' and product_count == 0:
        category.delete()
        messages.success(request, f'Category "{category.name}" deleted successfully.')
        return redirect('category_list')

    return render(request, 'products/delete_category.html', {
        'category': category,
        'product_count': product_count,
    })

