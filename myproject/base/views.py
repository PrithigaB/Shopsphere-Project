from django.shortcuts import render,redirect
from .models import Products,CartModel
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Sum
from .models import CartModel




# Create your views here.

def home(request):
    nomatch = False
    all_products = Products.objects.all()

    if 'q' in request.GET:
        q = request.GET['q']
        all_products = all_products.filter(
            Q(pname__icontains=q) | Q(pdesc__icontains=q)
        )
        if not all_products:
            nomatch = True

    if 'cat' in request.GET:
        all_products = all_products.filter(pcategory=request.GET['cat'])

    if 'trending' in request.GET:
        all_products = all_products.filter(trending=True)

    if 'offer' in request.GET:
        all_products = all_products.filter(offer=True)

    category = Products.objects.values_list('pcategory', flat=True).distinct()

    return render(request, 'home.html', {
        'all_products': all_products,
        'nomatch': nomatch,
        'category': category,
        'cart_count': get_cart_count(request),  

    })



@login_required
def addtocart(request, pk):
    product = Products.objects.get(id=pk)

    cart_item, created = CartModel.objects.get_or_create(
        pname=product.pname,
        host=request.user,
        defaults={
            'price': product.price,
            'pcategory': product.pcategory,
            'quantity': 1,
            'totalprice': product.price
        }
    )

    if not created:
        cart_item.quantity += 1
        cart_item.totalprice = cart_item.quantity * cart_item.price
        cart_item.save()

    return redirect('cart')


@login_required
def increase_qty(request, id):
    item = CartModel.objects.get(id=id)
    item.quantity += 1
    item.totalprice = item.quantity * item.price
    item.save()
    return redirect('cart')

@login_required
def decrease_qty(request, id):
    item = CartModel.objects.get(id=id)
    if item.quantity > 1:
        item.quantity -= 1
        item.totalprice = item.quantity * item.price
        item.save()
    else:
        item.delete()
    return redirect('cart')





@login_required
def cart(request):
    cartproducts = CartModel.objects.filter(host=request.user)
    total = sum(i.totalprice for i in cartproducts)
    return render(request,'cart.html',{
        'cartproducts':cartproducts,
        'total':total,
        'cart_count': get_cart_count(request), 
    })





def get_cart_count(request):
    if request.user.is_authenticated:
        # Sum the quantity of all cart items for this user
        return CartModel.objects.filter(host=request.user).aggregate(
            total=Sum('quantity')
        )['total'] or 0
    return 0




def support(request):
    return render(request, 'support.html', {
        'cart_count': get_cart_count(request)
    })



def know_us(request):
    return render(request, 'know_us.html', {
        'cart_count': get_cart_count(request)
    })
