from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from django.contrib import messages
from .models import Product, Category
from .forms import ProductForm, CategoryForm

def home(request):
    return render(request, 'products/home.html')

def product_list(request):
    products = Product.objects.all()
    search_query = request.GET.get('q', '')
    
    if search_query:
        products = products.filter(name__icontains=search_query)
    
    context = {'products': products, 'search_query': search_query}
    return render(request, 'products/product_list.html', context)

def add_product(request):
    """View to create a new product with full validation."""
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" created successfully!')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
    
    context = {'form': form, 'title': 'Add New Product'}
    return render(request, 'products/add_product.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'products/product_detail.html', context)

def edit_product(request, pk):
    """View to edit an existing product with full validation."""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" updated successfully!')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    
    context = {'form': form, 'title': f'Edit {product.name}', 'product': product}
    return render(request, 'products/edit_product.html', context)

def delete_product(request, pk):
    """View to delete a product with confirmation - POST only."""
    product = get_object_or_404(Product, pk=pk)
    
    # Only allow DELETE via POST method
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully!')
        return redirect('product_list')
    
    # Show confirmation page for GET requests
    context = {'product': product}
    return render(request, 'products/delete_product.html', context)

def category_list(request):
    categories = Category.objects.annotate(product_count=Count('products'))
    context = {'categories': categories}
    return render(request, 'products/category_list.html', context)

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    context = {'category': category, 'products': products}
    return render(request, 'products/category_products.html', context)

def add_category(request):
    """View to create a new category with full validation."""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" created successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm()
    
    context = {'form': form, 'title': 'Add New Category'}
    return render(request, 'products/add_category.html', context)

def edit_category(request, slug):
    """View to edit an existing category with full validation."""
    category = get_object_or_404(Category, slug=slug)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" updated successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    
    context = {'form': form, 'title': f'Edit {category.name}', 'category': category}
    return render(request, 'products/edit_category.html', context)

def delete_category(request, slug):
    """View to delete a category with confirmation - POST only."""
    category = get_object_or_404(Category, slug=slug)
    
    # Check if category has products
    product_count = category.products.count()
    
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f'Category "{category_name}" deleted successfully!')
        return redirect('category_list')
    
    context = {'category': category, 'product_count': product_count}
    return render(request, 'products/delete_category.html', context)

def about(request):
    return render(request, 'products/about.html')
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>404 - Page Not Found</title>
        
    </head>
    <body>
        <div class="container">
            <h1>404</h1>
            <h2>Page Not Found</h2>
            <div class="error-message">
                <p>Sorry! The page you're looking for doesn't exist or has been moved.</p>
            </div>
            <p>The requested URL was not found on this server.</p>
            <p>Let's get you back on track:</p>
            <p>
                <a href="/">← Home</a> | 
                <a href="/products/">Products</a> | 
                <a href="/about/">About Us</a>
            </p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content, status=404)
