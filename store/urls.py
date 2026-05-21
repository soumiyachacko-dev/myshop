from django.urls import path
from store import views
urlpatterns = [
    path('', views.home_view, name='home'),
    path('product_detail/<int:id>/', views.product_detail_view, name='product_detail'),
    path('category/<int:id>/', views.category_view, name='category'),
    path('search/', views.search_view, name='search'),
    path('cart/', views.cart_view, name='cart'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='custom_logout'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase/<int:id>/', views.increase_qty, name='increase_qty'),
    path('decrease/<int:id>/', views.decrease_qty, name='decrease_qty'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('order_detail/<int:id>/', views.order_details, name='order_detail'),
]