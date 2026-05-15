from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect

from apps.models import User, ToDo


def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email)
        if not user.exists():
            messages.warning(request, 'Diqqat bundey email topilmadi !')
            return redirect('login')
        user_data = user.first()
        if not check_password(password, user_data.password):
            messages.error(request, "Parol xato kiritildi !")
            return redirect('login')
        login(request, user_data)
        messages.success(request, f"Assalomu alaykum,{user_data.first_name} sizni ToDolaringiz kutib qoldi")
        return redirect('home')
    else:
        return render(request, 'Login.html')


def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email)
        if user.exists():
            messages.error(request, "Bundey email allaqochon mavjud")
            return redirect('register')
        User.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password)
        messages.success(request, "Ro'yxatdan muvaffaqiyatli o'tdingiz!")
        return redirect('login')
    else:
        return render(request, 'Register.html')


@login_required
def home_view(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        category = request.POST.get('category')
        ToDo.objects.create(title=title, desc=description, status=status, cate=category, user=request.user)
        messages.success(request, 'Hammasi alo qoshildi')
        return redirect('home')
    user_todo = request.user.tasks.all().order_by('created_at')
    user_todo_count = request.user.tasks.all().count()
    user_todo_succes = request.user.tasks.filter(status="Bajarildi").count()
    user_todo_other = user_todo_count - user_todo_succes

    context = {
        "user_todo": user_todo,
        "user_todo_count": user_todo_count,
        "user_todo_succes": user_todo_succes,
        "user_todo_other": user_todo_other
    }
    return render(request, 'Home.html', context)


def edit_view(request, id):
    if request.method == "GET":
        todos = ToDo.objects.filter(id=id).first()
        return render(request, 'Edit.html', {"todos": todos})
    else:
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        category = request.POST.get('category')
        ToDo.objects.filter(id=id).update(title=title, desc=description, status=status, cate=category)
        messages.success(request, f"{id}-Muffaqiyatli tahrirlandi !")
        return redirect('home')


def delete_view(request, id):
    ToDo.objects.filter(id=id).delete()
    messages.success(request, f"{id} - Muffaqtiyatli o'chirildi")
    return redirect('home')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
