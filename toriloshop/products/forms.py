from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    """Form for creating and updating products with full validation."""
    
    class Meta:
        model = Product
        fields = ['name', 'price', 'stock', 'category']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name',
                'maxlength': '200'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price (e.g., 99.99)',
                'step': '0.01',
                'min': '0.01'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter stock quantity',
                'min': '0'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
    
    # Custom validation for name field
    def clean_name(self):
        name = self.cleaned_data.get('name')
        
        # Check if name is provided
        if not name:
            raise forms.ValidationError("Product name is required.")
        
        # Strip whitespace
        name = name.strip()
        
        # Check minimum length
        if len(name) < 3:
            raise forms.ValidationError("Product name must be at least 3 characters long.")
        
        # Check maximum length
        if len(name) > 200:
            raise forms.ValidationError("Product name cannot exceed 200 characters.")
        
        # Check for valid characters (letters, numbers, spaces, hyphens, underscores)
        import re
        if not re.match(r'^[\w\s\-]+$', name):
            raise forms.ValidationError("Product name can only contain letters, numbers, spaces, hyphens, and underscores.")
        
        # Check for duplicate name (excluding current instance if editing)
        if Product.objects.filter(name__iexact=name).exclude(pk=self.instance.pk if self.instance.pk else None).exists():
            raise forms.ValidationError("A product with this name already exists.")
        
        return name
    
    # Custom validation for price field
    def clean_price(self):
        price = self.cleaned_data.get('price')
        
        # Check if price is provided
        if price is None:
            raise forms.ValidationError("Product price is required.")
        
        # Check if price is positive
        if price <= 0:
            raise forms.ValidationError("Product price must be greater than zero.")
        
        # Check for reasonable price range
        if price > 999999.99:
            raise forms.ValidationError("Product price cannot exceed 999,999.99.")
        
        return price
    
    # Custom validation for stock field
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        
        # Check if stock is provided
        if stock is None:
            raise forms.ValidationError("Stock quantity is required.")
        
        # Check if stock is non-negative
        if stock < 0:
            raise forms.ValidationError("Stock quantity cannot be negative.")
        
        # Check for reasonable stock range
        if stock > 999999:
            raise forms.ValidationError("Stock quantity cannot exceed 999,999.")
        
        return stock
    
    # Custom validation for category field
    def clean_category(self):
        category = self.cleaned_data.get('category')
        
        # Check if category is provided
        if not category:
            raise forms.ValidationError("Please select a category.")
        
        # Verify category exists
        if not Category.objects.filter(pk=category.pk).exists():
            raise forms.ValidationError("Selected category does not exist.")
        
        return category


class CategoryForm(forms.ModelForm):
    """Form for creating and updating categories with full validation."""
    
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'auto-generated if empty'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category description (optional)',
                'rows': 3
            }),
        }
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        
        if not name:
            raise forms.ValidationError("Category name is required.")
        
        name = name.strip()
        
        if len(name) < 2:
            raise forms.ValidationError("Category name must be at least 2 characters long.")
        
        if len(name) > 100:
            raise forms.ValidationError("Category name cannot exceed 100 characters.")
        
        import re
        if not re.match(r'^[\w\s\-]+$', name):
            raise forms.ValidationError("Category name can only contain letters, numbers, spaces, hyphens, and underscores.")
        
        if Category.objects.filter(name__iexact=name).exclude(pk=self.instance.pk if self.instance.pk else None).exists():
            raise forms.ValidationError("A category with this name already exists.")
        
        return name
    
    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        
        if slug:
            slug = slug.strip().lower()
            
            import re
            if not re.match(r'^[a-z0-9\-]+$', slug):
                raise forms.ValidationError("Slug can only contain lowercase letters, numbers, and hyphens.")
            
            if Category.objects.filter(slug=slug).exclude(pk=self.instance.pk if self.instance.pk else None).exists():
                raise forms.ValidationError("A category with this slug already exists.")
            
            return slug
        
        # Auto-generate slug from name if not provided
        from django.utils.text import slugify
        name = self.cleaned_data.get('name')
        if name:
            return slugify(name.strip())
        
        return slug
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        
        if description:
            description = description.strip()
            if len(description) > 500:
                raise forms.ValidationError("Description cannot exceed 500 characters.")
        
        return description