import json
import razorpay
import google.generativeai as genai
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import * 
from django.shortcuts import get_object_or_404
from .models import Cart, Product
from .models import Order

# Ye line initiate_payment ke upar honi chahiye
client = razorpay.Client(auth=("rzp_test_SknKwzX098VXi6", "zaXj27VnNgc6d1Cec3ZIzQBO"))


# ------------------ HOME & PROFILE ------------------

def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

@login_required
def profile(request):
    user = request.user
    if request.method == "POST":
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()
    return render(request, 'profile.html')

@login_required
def dashboard(request):
    user = request.user
    context = {
        'orders': Order.objects.filter(user=user),
        'appointments': Appointment.objects.filter(user=user),
        'labtests': LabTestOrder.objects.filter(user=user),
        'memberships': Membership.objects.filter(user=user),
    }
    return render(request, 'dashboard.html', context)

# ------------------ MEDICINE CART & DATABASE SYNC ------------------

def add_to_cart(request, product_id):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'Login karein'}, status=401)
            
        product = get_object_or_404(Product, id=product_id)
        
        # Admin panel mein data save karne ka main logic
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product
        )
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
            
        return JsonResponse({'status': 'success'})

@login_required
def cart(request):
    items = Cart.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, 'cart.html', {'items': items, 'total': total})

# ------------------ RAZORPAY PAYMENT GATEWAY ------------------

@login_required
def initiate_payment(request):
    if request.method == "POST":
        try:
            # 1. Frontend se JSON data nikalna
            data = json.loads(request.body)
            name = data.get('name')
            phone = data.get('phone')
            address = data.get('address')
            amount = data.get('amount')

            if not amount or float(amount) == 0:
                return JsonResponse({'status': 'error', 'message': 'Cart is empty'}, status=400)

            # 2. Database (Admin Panel) mein Order save karna
            # Isse "0 order" wali problem solve ho jayegi
            new_order = Order.objects.create(
                user=request.user,
                full_name=name,
                phone_number=phone,
                address=address,
                total_amount=float(amount),
                status="Pending"
            )

            # 3. Razorpay Order create karna
            # Razorpay ko paise (amount * 100) mein chahiye hote hain
            razor_data = {
                "amount": int(float(amount) * 100), 
                "currency": "INR",
                "payment_capture": "1"
            }
            razorpay_order = client.order.create(data=razor_data)

            # 4. Frontend ko dono IDs bhej dena
            return JsonResponse({
                "id": razorpay_order['id'], # Razorpay ID
                "amount": razorpay_order['amount'],
                "db_order_id": new_order.id, # Aapka Database ID
                "status": "success"
            })

        except Exception as e:
            print(f"Error: {e}") # Terminal mein error dekhne ke liye
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)



@csrf_exempt
def payment_handler(request): # Pehle iska naam 'payment_success' tha
    """Payment verify karke Order save karne ke liye"""
    if request.method == "POST":
        res_data = request.POST
        params_dict = {
            'razorpay_order_id': res_data.get('razorpay_order_id'),
            'razorpay_payment_id': res_data.get('razorpay_payment_id'),
            'razorpay_signature': res_data.get('razorpay_signature')
        }

        try:
            client.utility.verify_payment_signature(params_dict)
            
            # Database update logic
            user = request.user
            cart_items = Cart.objects.filter(user=user)
            total = sum(item.product.price * item.quantity for item in cart_items)
            
            # Order create karein
            Order.objects.create(user=user, total_amount=total, status="Paid")
            
            # Cart clear karein
            cart_items.delete()
            
            return redirect('order_success')
        except Exception as e:
            print(f"Payment Error: {e}") # Terminal mein error check karein
            return render(request, 'payment_failed.html')

# ------------------ DOCTOR & LAB TESTS ------------------

@login_required
def book_appointment(request):
    if request.method == "POST":
        Appointment.objects.create(
            user=request.user, 
            doctor_name=request.POST.get('doctor'),
            specialization=request.POST.get('specialization'),
            date=request.POST.get('date'),
            time=request.POST.get('time')
        )
        return redirect('order_success')
    return render(request, 'finddoctors.html')

@csrf_exempt
@login_required
def place_lab_order(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            order = LabTestOrder.objects.create(
                user=request.user,
                test_names=data.get('items_list'), 
                total_amount=data.get('total_price'),
                status="Pending"
            )
            return JsonResponse({"status": "success", "order_id": order.id})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

# ------------------ MISC & AUTH ------------------

def register_view(request):
    if request.method == "POST":
        u, e, p = request.POST.get('username'), request.POST.get('email'), request.POST.get('password')
        if User.objects.filter(username=u).exists():
            return render(request, 'register.html', {'error': 'User already exists'})
        user = User.objects.create_user(username=u, email=e, password=p)
        login(request, user)
        return redirect('home')
    return render(request, 'register.html')

def my_order(request):
    return render(request, 'myorder.html', {'razorpay_key': settings.RAZORPAY_KEY_ID})

@csrf_exempt
def order_success(request):

    payment_id = request.POST.get("razorpay_payment_id")

    return render(request, "order_success.html", {
        "payment_id": payment_id
    })

def success(request):
    return render(request, 'success.html')

# views.py mein niche add karein

def add_lab_test(request):
    # Abhi ke liye sirf render karein, logic baad mein add kar sakte hain
    return render(request, 'labtests.html')

def buy_membership(request):
    return render(request, 'circlemembership.html')

def health(request):
    return render(request, 'health.html')

def map(request):
    return render(request, 'map.html')

