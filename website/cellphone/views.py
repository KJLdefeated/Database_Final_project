from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from datetime import datetime
from .models import Users
from .models import Data
from .models import Rate

def home(request):
    return render(request, 'main.html')

def operation(request):
    return render(request, 'operation.html')

def get_users(request):
    users = Users.objects.all()
    return JsonResponse({'all': list(users.values())})

def get_data(request):
    data = Data.objects.all()
    return JsonResponse({'all': list(data.values())})

def get_rate(request):
    rate = Rate.objects.all()
    return JsonResponse({'all': list(rate.values())})

def register(request):
    if request.method == 'POST':
        id = request.POST['id']
        age = request.POST.get('age')
        gender = request.POST['gender']
        occupation = request.POST['occupation']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if Users.objects.filter(user_id=id).exists():
                messages.info(request, 'Username Alredy Used')
                return redirect('/operation/')
            else:
                user = Users(user_id = id,age = age, gender = gender, occupation = occupation, password = password)
                user.save()
                return redirect('/login/')
        else:
            messages.info(request, 'Password Not The Same.')
            return redirect('/register/')
    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        id = request.POST['id']
        password = request.POST['password']
        if Users.objects.filter(user_id = id, password = password).exists():
            request.session['user_id'] = id
            return redirect('/operation/')
        else:
            messages.info(request, 'The User ID or password may be wrong.')
            return redirect('/login/')
    return render(request, 'login.html')
    
def rating(request):
    if request.method == 'POST':
        id = request.session['user_id']
        cellphone_id = request.POST['cellphone']
        rate = request.POST['rate']
        if Rate.objects.filter(user_id=id, cellphone_id=cellphone_id).exists():
            messages.info(request, 'You have rated this cellphone.')
            return redirect('/rating/')
        else:
            user = Users.objects.get(user_id=id)
            if Data.objects.filter(cellphone_id=cellphone_id).exists():
                cellphone = Data.objects.get(cellphone_id=cellphone_id)
            else:
                messages.info(request, 'Doesnt  exist this cellphone.')
                return redirect('/rating/')
            newrate = Rate(user = user,cellphone=cellphone,rating = rate)
            newrate.save()
            return redirect('/operation/')
    return render(request, 'rating.html')