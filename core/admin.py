from django.contrib import admin
from .models import Product, Cart, Order, Appointment, LabTest, Membership

# 1. Appointment Model ke liye Table View setup
class AppointmentAdmin(admin.ModelAdmin):
    # Yeh columns Admin Panel ki list mein dikhenge
    list_display = ('id', 'user', 'doctor_name', 'specialization', 'date', 'time')
    
    # Isse aap side mein user ya date ke hisaab se filter kar sakte hain
    list_filter = ('user', 'date')
    
    # Isse aap doctor ke naam se search kar sakte hain
    search_fields = ('doctor_name', 'user__username')

# 2. Models ko Register karna (Sirf ek-ek baar)

# Appointment ko advanced view ke saath register karein
admin.site.register(Appointment, AppointmentAdmin)

# Baki models ko normal register karein
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(LabTest)
admin.site.register(Membership)