from django.shortcuts import render, redirect
from django.contrib import messages  # для сообщений об ошибке
from .models import Order, Product  # предполагаем, что есть модель Product
from .forms import OrderForm
from django.contrib.auth.decorators import login_required

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/my_orders.html", {"orders": orders})

def checkout(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()

            # Проверка stock через items
            for item in order.items.all():
                if item.quantity > item.product.stock:
                    messages.error(request, f"Нельзя заказать больше, чем есть на складе: {item.product.name}")
                    return redirect("cart")

            messages.success(request, "Заказ успешно оформлен!")
            return redirect("order_success")
    else:
        form = OrderForm()

    return render(request, "orders/checkout.html", {"form": form})