from django.urls import path
from . import views

urlpatterns = [
    # --- Home & Auth ---
    path('', views.index, name='home'),
    path('index/', views.index, name='home_index'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # --- Cart & Inventory ---
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    
    # --- Razorpay Payment Gateway (Updated) ---
    # Jab user checkout button dabayega
    path('initiate-payment/', views.initiate_payment, name='initiate_payment'),
    
    # Jab Razorpay payment confirm karke wapas bhejega
    # Note: views.py mein function ka naam 'payment_handler' hai toh wahi likhein
    path('payment-handler/', views.payment_handler, name='payment_handler'), 

    # --- Success & Orders ---
    path('my-order/', views.my_order, name='myorder'),
    path('order-success/', views.order_success, name='order_success'),
    path('success/', views.success, name='success'), # General success page

    # --- Lab Tests & Appointments ---
    path('lab-test/', views.add_lab_test, name='lab_test'),
    path('place-lab-order/', views.place_lab_order, name='place_lab_order'),
    path('booking-success/<int:appointment_id>/', views.booking_success, name='booking_success'),
    path('membership/', views.buy_membership, name='membership'),
    path('health/', views.health, name='health'),
    path('map/', views.map, name='map'),

]