from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserForm, CustomUserCreationForm, StaffVendorForm
from django.contrib.auth.decorators import login_required
from app.decorators import for_admins
from .models import CustomUser

def signup_user(request):
    if request.method == 'GET':
        form = CustomUserCreationForm()
        return render(request, 'registration/signup.html', context={'form': form})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, 'registration/signup.html', context={'form': form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid matric number or password")
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
@for_admins
def add_user(request):
    if request.method == 'GET':
        form = AddUserForm()
        return render(request, 'add_user.html', context={'form': form})
    elif request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, 'add_user.html', context={'form': form})

@for_admins
@login_required(login_url='login')
def edit_user(request, id):
    user = get_object_or_404(CustomUser, id=id)
    user_fullname = CustomUser.objects.get(id=id).full_name
    if user.user_type == 'staff' or 'vendor':
        form = StaffVendorForm(instance=user)
        if request.method == 'POST':
            form = StaffVendorForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
    else:
        form = UserForm(instance=user)
        if request.method == 'POST':
            form = UserForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
    return render(request, 'edit_user.html', {'form': form, 'id': id, 'user_fullname': user_fullname})


@login_required(login_url='login')
@for_admins
def delete_user(request, id):
    user = CustomUser.objects.get(id=id)
    user.delete()
    return redirect('dashboard')

@login_required(login_url='login')
def all_students(request):
    search_input = request.GET.get('search')
    if search_input == None:
        students = CustomUser.objects.filter(user_type='student')
    else:
        students = CustomUser.objects.filter(full_name__icontains=search_input)
    return render(request, 'students.html', {'students' : students})

@login_required(login_url='login')
def all_staff(request):
    search_input = request.GET.get('search')
    if search_input == None:
        staff = CustomUser.objects.filter(user_type='staff')
    else:
        staff = CustomUser.objects.filter(full_name__icontains=search_input)
    return render(request, 'staff.html', {'staff' : staff})

@login_required(login_url='login')
def all_vendors(request):
    search_input = request.GET.get('search')
    if search_input == None:
        vendors = CustomUser.objects.filter(user_type='vendor')
    else:
        vendors = CustomUser.objects.filter(full_name__icontains=search_input)
    return render(request, 'vendors.html', {'vendors' : vendors})



