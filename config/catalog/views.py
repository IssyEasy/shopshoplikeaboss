from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Category, Product

def home(request):
    categories = Category.objects.all()
    return render(request, "catalog/home.html", {"categories": categories})

def category_list(request):
    categories = Category.objects.all()
    return render(request, "catalog/category_list.html", {"categories": categories})

def product_list_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True).order_by("name")

    paginator = Paginator(products, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "catalog/product_list.html", {"category": category, "page_obj": page_obj})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, "catalog/product_detail.html", {"product": product})