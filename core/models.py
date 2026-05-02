from django.db import models
from django.contrib.auth.models import User


# Medicine Product
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name


# Cart
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


# Order
from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    # Citation ([cite: 1]) ko yahan se hata dein
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    
    # Nayi fields jo aapne add ki hain
    full_name = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    
    # Existing fields
    total_amount = models.FloatField()
    status = models.CharField(max_length=50, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.full_name}"
    
# Doctor Appointment
class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    def __str__(self):
        return f"{self.user.username} - {self.doctor_name}"
    


# Lab Test Booking
class LabTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=200)
    price = models.FloatField()
    booked_on = models.DateTimeField(auto_now_add=True)


# Circle Membership
class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=100)
    price = models.FloatField()
    active = models.BooleanField(default=True)


    # core/models.py

class Appointment(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    doctor_name = models.CharField(max_length=200)

    specialization = models.CharField(max_length=200)

    date = models.DateField()

    time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    def __str__(self):
        return f"{self.user.username} - {self.doctor_name}"


class LabTestOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test_names = models.TextField()  # Saare tests ke naam yahan store honge
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="Pending")

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    
    from django.db import models

class Transaction(models.Model):
    patient_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_id = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    