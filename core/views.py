from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from .forms import RegisterForm, ProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'core/home.html')


import json
from django.http import JsonResponse
from .models import Form, FormField



def form_builder(request):
    if request.method == "POST":
        title = "Custom Form"  
        form = Form.objects.create(title=title)

        labels = request.POST.getlist('labels[]')
        types = request.POST.getlist('types[]')

        for index, (label, ftype) in enumerate(zip(labels, types)):
            FormField.objects.create(
                form=form,
                label=label,
                field_type=ftype,
                order=index
            )

        return redirect("core:form_preview", form_id=form.id)


    return render(request, "core/form_builder.html")

def form_preview(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    return render(request, "core/form_preview.html", {"form": form})



def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created. Please login.')
            return redirect('core:login')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('core:home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('core:login')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('core:profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'core/profile.html', {'form': form})

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # keep user logged in
            messages.success(request, 'Password updated.')
            return redirect('core:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'core/change_password.html', {'form': form})


from .models import Employee

@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, "core/employee_list.html", {"employees": employees})

@login_required
def employee_create(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        department = request.POST.get("department", "")  # ✅ safe
        position = request.POST.get("position", "")      # ✅ safe

        Employee.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            department=department,
            position=position,
        )
        return redirect("core:employee_list")
    return render(request, "core/employee_form.html")

@login_required
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        employee.first_name = request.POST["first_name"]
        employee.last_name = request.POST["last_name"]
        employee.email = request.POST["email"]
        employee.save()
        return redirect("core:employee_list")
    return render(request, "core/employee_form.html", {"employee": employee})

@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        employee.delete()
        return redirect("core:employee_list")
    return render(request, "core/employee_confirm_delete.html", {"employee": employee})


