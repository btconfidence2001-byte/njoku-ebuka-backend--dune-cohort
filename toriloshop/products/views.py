from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("Welcome to Torilo Shop! Your one-stop store for amazing products🛒🛒🛒.")
def product_list(request):
    return HttpResponse(
        "Here is a list of all our available products. Browse and shop to your heart's content!"+
        "print()"
        )
def about(request):
    return HttpResponse("Welcome to Torilo Shop! Your one-stop store for amazing products.")

def custom_404(request, exception):
    return HttpResponse("Page not found - Sorry, the page you are looking for does not exist.", status=404)