from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from datetime import datetime
from .models import Users
from .models import Data
from .models import Rate
import psycopg2

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

def cellphone_avg_rate(request):
    conn = None
    
    conn = psycopg2.connect(
        host="database-2.cahrpukjz3tx.us-east-1.rds.amazonaws.com",
        database="postgres",
        user="postgres",
        password="umamusume")
    cur = conn.cursor()
    cur.execute("""
            (select 'average' as model,round(cast(avg(rating) as decimal),3) as average from rate,data)
            union
            (select model,newt.average
            from(select cellphone_id,round(cast(avg(rating) as decimal),3) as average
            from rate
            group by cellphone_id) as newt,data
            where newt.cellphone_id=data.cellphone_id)
            order by average desc;
    """)
    data = cur.fetchall()
    processedData = []
    column_names = [desc[0] for desc in cur.description]
    for i in range(len(data)):
        row = {}
        for j in range(len(column_names)):
            row[column_names[j]] = data[i][j]
        processedData.append(row)

    if conn is not None:
        re = JsonResponse({'all': processedData})
        conn.close()
    return re
def market_share(request):
    conn = None
    
    conn = psycopg2.connect(
        host="database-2.cahrpukjz3tx.us-east-1.rds.amazonaws.com",
        database="postgres",
        user="postgres",
        password="umamusume")
    cur = conn.cursor()
    cur.execute("""
            with brand_amount(brand,amount) as
(select data.brand, count(*) as amount 
from data
join rate on data.cellphone_id=rate.cellphone_id
group by data.brand
order by amount desc)

select brand_amount.brand,
concat(round(cast(brand_amount.amount as decimal)/9.9,2),'%') as market_share
from brand_amount
order by brand_amount.amount desc

    """)
    data = cur.fetchall()
    processedData = []
    column_names = [desc[0] for desc in cur.description]
    for i in range(len(data)):
        row = {}
        for j in range(len(column_names)):
            row[column_names[j]] = data[i][j]
        processedData.append(row)

    if conn is not None:
        re = JsonResponse({'all': processedData})
        conn.close()
    return re
def avg_sex_M(request):
    conn = None
    
    conn = psycopg2.connect(
        host="database-2.cahrpukjz3tx.us-east-1.rds.amazonaws.com",
        database="postgres",
        user="postgres",
        password="umamusume")
    cur = conn.cursor()
    cur.execute("""
            select data.model,tablelast.average_rating,tablelast.number_of_ratings
from(select cellphone_id,round(cast(avg(rating) as decimal),3) as average_rating,count(user_id) as number_of_ratings
from (select * from(select * from rate NATURAL join users) as bigT where gender='Male')as newbigT
group by cellphone_id)as tablelast,data
where tablelast.cellphone_id=data.cellphone_id
order by tablelast.average_rating desc;


    """)
    data = cur.fetchall()
    processedData = []
    column_names = [desc[0] for desc in cur.description]
    for i in range(len(data)):
        row = {}
        for j in range(len(column_names)):
            row[column_names[j]] = data[i][j]
        processedData.append(row)

    if conn is not None:
        re = JsonResponse({'all': processedData})
        conn.close()
    return re
def avg_sex_F(request):
    conn = None
    
    conn = psycopg2.connect(
        host="database-2.cahrpukjz3tx.us-east-1.rds.amazonaws.com",
        database="postgres",
        user="postgres",
        password="umamusume")
    cur = conn.cursor()
    cur.execute("""
            select data.model,tablelast.average_rating,tablelast.number_of_ratings
from(select cellphone_id,round(cast(avg(rating) as decimal),3) as average_rating,count(user_id) as number_of_ratings
from (select * from(select * from rate NATURAL join users) as bigT where gender='Female')as newbigT
group by cellphone_id)as tablelast,data
where tablelast.cellphone_id=data.cellphone_id
order by tablelast.average_rating desc;


    """)
    data = cur.fetchall()
    processedData = []
    column_names = [desc[0] for desc in cur.description]
    for i in range(len(data)):
        row = {}
        for j in range(len(column_names)):
            row[column_names[j]] = data[i][j]
        processedData.append(row)

    if conn is not None:
        re = JsonResponse({'all': processedData})
        conn.close()
    return re
def top_elder(request):
    conn = None
    
    conn = psycopg2.connect(
        host="database-2.cahrpukjz3tx.us-east-1.rds.amazonaws.com",
        database="postgres",
        user="postgres",
        password="umamusume")
    cur = conn.cursor()
    cur.execute("""
            select data.model,newt.averageRate
from(select cellphone_id,round(cast(avg(rating) as decimal),3) as averageRate
from(select * from rate natural join (select user_id from
(select avg(age) as avg_age from users) as avgT,users
where users.age>avgT.avg_age) as newt) as bigT
group by cellphone_id
limit 10) as newt,data
where newt.cellphone_id=data.cellphone_id
order by newt.averageRate desc;

    """)
    data = cur.fetchall()
    processedData = []
    column_names = [desc[0] for desc in cur.description]
    for i in range(len(data)):
        row = {}
        for j in range(len(column_names)):
            row[column_names[j]] = data[i][j]
        processedData.append(row)

    if conn is not None:
        re = JsonResponse({'all': processedData})
        conn.close()
    return re