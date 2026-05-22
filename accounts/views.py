from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Product, WarehouseActivity
from .forms import ProductForm
from .models import Receiving
from .forms import ReceivingForm
from .models import Putaway, WarehouseActivity
from .forms import PutawayForm
from .models import Picking
from .forms import PickingForm
from .models import Packing
from .forms import PackingForm
from .models import Shipping
from .forms import ShippingForm
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_page(request):
    logout(request)
    return redirect('login')



# =========================
# REGISTER PAGE
# =========================
def register_page(request):

    if request.method == "POST":

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # PASSWORD CHECK
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        # USER EXISTS CHECK
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        # CREATE USER
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()

        messages.success(request, "Account created successfully. Please login.")
        return redirect('login')

    return render(request, 'accounts/register.html')


# =========================
# LOGIN PAGE
# =========================
def login_page(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)
            return redirect('dashboard')

        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'accounts/index.html')


# =========================
# DASHBOARD (REAL DATA)
# =========================
def dashboard(request):

    if not request.user.is_authenticated:
        return redirect('login')

    products_count = Product.objects.count()

    receiving = WarehouseActivity.objects.filter(activity_type='RECEIVING').count()
    putaway = WarehouseActivity.objects.filter(activity_type='PUTAWAY').count()
    inventory = Product.objects.count()
    picking = WarehouseActivity.objects.filter(activity_type='PICKING').count()
    packing = WarehouseActivity.objects.filter(activity_type='PACKING').count()
    shipping = WarehouseActivity.objects.filter(activity_type='SHIPPING').count()

    activities = WarehouseActivity.objects.all().order_by('-created_at')[:10]

    context = {
        'products_count': products_count,
        'receiving': receiving,
        'putaway': putaway,
        'inventory': inventory,
        'picking': picking,
        'packing': packing,
        'shipping': shipping,
        'activities': activities,
    }

    return render(request, 'accounts/dashboard.html', context)


# =========================
# LOGOUT
# =========================
def logout_page(request):
    logout(request)
    return redirect('login')


def add_product(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":

        form = ProductForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "Product added successfully")
            return redirect('dashboard')

    else:
        form = ProductForm()

    return render(request, 'accounts/add_product.html', {'form': form})

def receiving_page(request):

    if not request.user.is_authenticated:
        return redirect('login')

    form = ReceivingForm()

    if request.method == "POST":

        form = ReceivingForm(request.POST)

        if form.is_valid():

            data = form.save()

            # 🔥 CONNECT TO DASHBOARD SYSTEM
            WarehouseActivity.objects.create(
                activity_type='RECEIVING',
                reference=f"RCV-{data.sku}",
                status='COMPLETED'
            )

            messages.success(request, "Goods received successfully")
            return redirect('receiving')

        else:
            messages.error(request, "Please check form errors")

    records = Receiving.objects.all().order_by('-received_date')

    return render(request, 'accounts/receiving.html', {
        'form': form,
        'records': records
    })

def putaway_page(request):

    if not request.user.is_authenticated:
        return redirect('login')

    form = PutawayForm()

    if request.method == "POST":

        form = PutawayForm(request.POST)

        if form.is_valid():

            data = form.save()

            # 🔥 CONNECT TO DASHBOARD
            WarehouseActivity.objects.create(
                activity_type='PUTAWAY',
                reference=f"PUT-{data.sku}",
                status='COMPLETED'
            )

            messages.success(request, "Putaway completed successfully")
            return redirect('putaway')

    records = Putaway.objects.all().order_by('-created_at')

    return render(request, 'accounts/putaway.html', {
        'form': form,
        'records': records
    })

# views.py



def inventory_page(request):

    if not request.user.is_authenticated:
        return redirect('login')

    # HANDLE FORM SUBMISSION
    if request.method == "POST":
        form = ProductForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully")

            # 🔥 IMPORTANT: reload page to see changes
            return redirect('inventory')

        
        else:

          print(form.errors)   # 🔥 ADD THIS
          messages.error(request, form.errors)  # 🔥 SHOW REAL ERROR

    else:
        form = ProductForm()

    products = Product.objects.all().order_by('-created_at')
    low_stock = Product.objects.filter(quantity__lte=5)

    return render(request, 'accounts/inventory.html', {
        'form': form,
        'products': products,
        'low_stock': low_stock
    })
def picking_page(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        form = PickingForm(request.POST)

        if form.is_valid():
            data = form.save()

            # 🔥 CONNECT TO DASHBOARD
            WarehouseActivity.objects.create(
                activity_type='PICKING',
                reference=f"PICK-{data.order_reference}",
                status='IN_PROGRESS'
            )

            messages.success(request, "Picking task created successfully")
            return redirect('picking')

        else:
            messages.error(request, form.errors)

    else:
        form = PickingForm()

    records = Picking.objects.all().order_by('-created_at')

    return render(request, 'accounts/picking.html', {
        'form': form,
        'records': records
    })

def packing_page(request):

    if not request.user.is_authenticated:
        return redirect('login')

    form = PackingForm()

    if request.method == "POST":
        form = PackingForm(request.POST)

        if form.is_valid():
            data = form.save()

            # 🔥 CONNECT TO DASHBOARD
            WarehouseActivity.objects.create(
                activity_type='PACKING',
                reference=f"PK-{data.order_ref}",
                status='COMPLETED'
            )

            messages.success(request, "Packing completed successfully")
            return redirect('packing')

        else:
            messages.error(request, "Form is not valid")

    records = Packing.objects.all().order_by('-created_at')

    return render(request, 'accounts/packing.html', {
        'form': form,
        'records': records
    })

def shipping_page(request):

    if not request.user.is_authenticated:
        return redirect('login')

    form = ShippingForm()

    if request.method == "POST":
        form = ShippingForm(request.POST)

        if form.is_valid():
            data = form.save()

            # 🔥 reduce stock from inventory
            product = data.product
            product.quantity -= data.quantity
            product.save()

            # 🔥 update dashboard activity
            WarehouseActivity.objects.create(
                activity_type='SHIPPING',
                reference=f"SHP-{data.order_ref}",
                status='COMPLETED'
            )

            messages.success(request, "Shipment created successfully")
            return redirect('shipping')

        else:
            messages.error(request, "Form is not valid")

    records = Shipping.objects.all().order_by('-shipped_at')

    return render(request, 'accounts/shipping.html', {
        'form': form,
        'records': records
    })

def logout_page(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')

    return render(request, 'accounts/logout.html')
    