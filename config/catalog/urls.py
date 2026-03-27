from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    # --- Каталог ---
    path("", views.home, name="home"),
    path("categories/", views.category_list, name="category_list"),
    path("category/<slug:slug>/", views.product_list_by_category, name="product_list_by_category"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),

    # --- Корзина ---
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("cart/remove/<int:product_id>/", views.cart_remove, name="cart_remove"),
    path("cart/increase/<int:product_id>/", views.cart_increase, name="cart_increase"),
    path("cart/decrease/<int:product_id>/", views.cart_decrease, name="cart_decrease"),
]