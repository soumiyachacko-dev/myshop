from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, OrderItem,Order
from django.contrib.auth import login, authenticate, logout
from .forms import OrderForm

def home_view(request):
    products =Product.objects.all()
    return render(request, 'home.html',{'products':products})
def product_detail_view(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})
def category_view(request, id):
    category = get_object_or_404(Category, id=id)
    products = Product.objects.filter(category=category)
    return render(request, 'category.html', {'products': products, 'category': category})
def search_view(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(Q(name__icontains=query)|Q(description__icontains=query)|Q(category__name__icontains=query)).distinct()
        categories = Category.objects.filter(name__icontains=query)
        return render(request, 'search_results.html',{'products':products,'categories':categories,'query':query})

def add_to_cart(request,id):
     cart=request.session.get('cart',{})
     if str(id) in cart:
         cart[str(id)] = cart[str(id)] + 1
     else: cart[str(id)] = 1
     request.session['cart'] = cart
     return redirect('cart')
def remove_from_cart(request,id):
     cart=request.session.get('cart',{})
     if str(id) in cart:
         del cart[str(id)]
         request.session['cart'] = cart
         return redirect('cart')
def increase_qty(request,id):
      cart=request.session.get('cart',{})
      if str(id) in cart:
          cart[str(id)] = cart[str(id)] + 1
          request.session['cart'] = cart
          return redirect('cart')
def decrease_qty(request, id):
    cart = request.session.get('cart', {})
    if str(id) in cart:
        cart[str(id)] -= 1
        if cart[str(id)] <= 0:
            del cart[str(id)]
        request.session['cart'] = cart
    return redirect('cart')
def cart_view(request):
    cart=request.session.get('cart',{})
    items=[]
    total=0
    for product_id,qty in cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = product.price * qty
        total = total + subtotal
        items.append({'product':product,'qty':qty,'subtotal':subtotal})
    return render(request, 'cart.html',{'items':items,'total':total})
def register(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        if not username:
            messages.error(request, "Username is required")
            return render(request, 'register.html')

        if not email:
            messages.error(request, "Email is required")
            return render(request, 'register.html')

        if not password:
            messages.error(request, "Password is required")
            return render(request, 'register.html')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return render(request, 'register.html')

        # Create user
        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully. Please login.")
        return redirect('login')

    return render(request, 'register.html')
def logout_view(request):
    logout(request)
    return redirect('home')
def calculate_cart_total(cart):
    total = 0
    for product_id,qty in cart.items():
        product = Product.objects.get(id=product_id)
        total += qty * product.price
    return total
def checkout_view(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('home')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)

            if request.user.is_authenticated:
                order.user = request.user

            order.total_price = calculate_cart_total(cart)
            order.save()

            for product_id, qty in cart.items():
                product = Product.objects.get(id=product_id)
                OrderItem.objects.create(
                    product=product,
                    order=order,
                    quantity=qty,
                    price=product.price
                )

            request.session['cart'] = {}
            return render(request, 'checkout_success.html', {'order': order})

    else:
        form = OrderForm()

    return render(request, 'checkout.html', {
        'form': form,
        'total': calculate_cart_total(cart)
    })
@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {'orders':orders})
@login_required
def order_details(request, id):
    order = get_object_or_404(Order,id=id,user=request.user)
    items=order.items.all()
    return render(request, 'order_detail.html', {'order':order, 'items':items})





























# Create your views here.
