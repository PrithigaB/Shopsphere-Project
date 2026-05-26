from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from base.views import get_cart_count




# Create your views here.
def login_(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'login_.html', {'error': 'Invalid username or password'})

    return render(request, 'login_.html',{
    'cart_count': get_cart_count(request)
})



def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check username
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'Username already exists'
            })

        # Check email
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {
                'error': 'Email already exists'
            })

        # Create user
        User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        # Redirect after successful registration
        return redirect('login_')

    return render(request, 'register.html',{
    'cart_count': get_cart_count(request)
})



@login_required(login_url='login_')
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user,  'cart_count': get_cart_count(request)})

def logout_(request):
    logout(request)
    return redirect('login_')



def forgot_password(request):
    if request.method == "POST":
        username = request.POST['username']

        if User.objects.filter(username=username).exists():
            return redirect('reset_password')
        else:
            return render(request, 'forgot_password.html', {'error': 'User not found'})

    return render(request, 'forgot_password.html',{
    'cart_count': get_cart_count(request)
})



def reset_password(request):
    if request.method == "POST":
        username = request.POST['username']
        new_password = request.POST['new_password']

        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()

        return redirect('login_')

    return render(request, 'reset_password.html',{
    'cart_count': get_cart_count(request)
})




@login_required(login_url='login_')
def update_password(request):
    if request.method == "POST":
        new_password = request.POST['new_password']
        request.user.set_password(new_password)
        request.user.save()
        return redirect('login_')

    return render(request, 'update_password.html',{
    'cart_count': get_cart_count(request)
})




@login_required(login_url='login_')
def update_profile(request):
    user = request.user

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')

        user.save()
        return redirect('profile')

    return render(request, 'update_profile.html',{
    'cart_count': get_cart_count(request)
})









'''
1.register
2.login
3.logout
4.profile
5.reset password
6.forgot password
7.update password
'''