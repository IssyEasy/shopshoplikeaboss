from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Category, Product
from django.db.models import Q
from decimal import Decimal, InvalidOperation

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

def product_list_by_category(request, slug):
    # Получаем категорию
    catalog_obj = get_object_or_404(Category, slug=slug)

    # Базовый QuerySet — активные товары этой категории
    qs = Product.objects.filter(category=catalog_obj, is_active=True)
    qs = qs.select_related("category").prefetch_related("images")

    # Поиск по названию и описанию
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))

    # Фильтр по цене
    min_price = request.GET.get("min_price", "").strip()
    max_price = request.GET.get("max_price", "").strip()
    try:
        if min_price:
            qs = qs.filter(price__gte=Decimal(min_price))
        if max_price:
            qs = qs.filter(price__lte=Decimal(max_price))
    except (InvalidOperation, ValueError):
        pass  # игнорируем некорректные значения

    # Фильтр по наличию
    if request.GET.get("in_stock") == "1":
        qs = qs.filter(stock__gt=0)

    # Сортировка
    sort = request.GET.get("sort", "")
    if sort == "price_asc":
        qs = qs.order_by("price")
    elif sort == "price_desc":
        qs = qs.order_by("-price")
    elif sort == "new":
        qs = qs.order_by("-id")  # новинки сверху
    else:
        qs = qs.order_by("name")

    # Пагинация
    paginator = Paginator(qs, 8)  # 8 товаров на страницу
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # GET-параметры для сохранения фильтров при переходе страниц
    params = request.GET.copy()
    params.pop("page", None)
    qs_params = params.urlencode()

    # Возврат результата
    return render(request, "catalog/product_list.html", {
        "catalog": catalog_obj,
        "page_obj": page_obj,
        "qs_params": qs_params,
    })