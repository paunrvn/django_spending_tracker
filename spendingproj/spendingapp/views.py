from django.http import  HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .models import Expense
from .forms import ExpenseForm
from datetime import datetime, timedelta
import csv

# Create your views here.
def spending(request):
    category = ""
    # Today button
    if request.GET.get('today'):
        value = request.GET.get('today')
        spendings = Expense.objects.filter(data=value).order_by('data')

    # Month button
    elif request.GET.get('month'):
        value = request.GET.get('month')
        spendings = Expense.objects.filter(data__month=value).order_by('data')

    # Week button
    elif request.GET.get('week'):
        value =  request.GET.get('week')
        year, week_number = map(int, value.split("-W"))
        start_of_week =  datetime.strptime(f'{year}-W{week_number}-1','%Y-W%W-%w').date()
        end_of_week = start_of_week + timedelta(days=6)
        spendings = Expense.objects.filter(data__range=[start_of_week, end_of_week]).order_by('data')

    # "Select day" button
    elif request.GET.get('day'):
        value =  request.GET.get('day')
        spendings = Expense.objects.filter(data=value).order_by('data')

    # "Select range" button
    elif request.GET.get('start_date') and request.GET.get('end_date'):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        spendings = Expense.objects.filter(data__range=[start_date, end_date]).order_by('data')

    # All time button
    else:
        spendings = Expense.objects.all()
        category = request.GET.get("category")
        if category:
            spendings = Expense.objects.filter(category=category).all()

    spendings_category = Expense.objects.all()
    categories = {spending.category for spending in spendings_category}

    now = datetime.now()
    today = {
        'value': now.strftime('%Y-%m-%d'),
        'display': now.day
    }
    month = {
        'value': now.strftime('%Y-%m-%d'),
        'display': now.month
    }
    first_day_of_week = now - timedelta(days=now.weekday())
    last_day_of_week = first_day_of_week + timedelta(days=6)
    week = {
        'first_day_of_week': first_day_of_week.strftime('%Y-%m-%d'),
        'last_day_of_week': last_day_of_week.strftime('%Y-%m-%d'),
        'display': first_day_of_week.strftime('%d' ' %b') + '-' + last_day_of_week.strftime('%d %b')
    }

    # aceasta linie calculeaza totalul atributelor Amount.
    total_amount = sum(spending.amount for spending in spendings)
    # aceasta linie randeaza template-ul spending.html
    # trimitand variabilele spendings si total_amount ca si context objects
    return render(request,"spending.html",
                   {"spendings":spendings,"total_amount":total_amount, "today":today, "month": month, "week":week,"categories":categories,"selected_category":category})

def adauga(request):
    # Cand utilizatorul acceseaza url/adauga, se va crea un obiect de tip form
    # si se va trimite spre template-ul html pentru randare
    if request.method == 'GET':
        form = ExpenseForm()
        return render(request, "adauga.html", {"form": form})
    # Request-urile de tip POST care vin pe url/adauga sunt facute sa fie procesate
    # si adaugate in baza de date
    elif request.method == 'POST':
        form = ExpenseForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect("/")

def export(request):
    expenses = Expense.objects.all()
    fieldnames = ['ID', 'Data', 'Vendor', 'Suma']
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'
    writer = csv.DictWriter(response, fieldnames=fieldnames)
    writer.writeheader()
    for expense in expenses:
        writer.writerow({
            'ID': expense.id,
            'Data': expense.data,
            'Vendor': expense.vendor,
            'Suma': expense.amount
        })
    return response


def select_day_data(request):
    return render(request,"select_day_data.html")


def select_range_data(request):
    return render(request,"select_range_data.html")

def edit(request,id):
    spending = Expense.objects.filter(id=id).first()
    data_edit = spending.data.strftime("%Y-%m-%d")
    if request.method == 'GET':
        return render(request, "edit.html",{"spending":spending,"data":data_edit})

    elif request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES,instance=spending)
        file = request.FILES.get("image")
        if not file:
            request.FILES.update({"image":spending.image})
            form = ExpenseForm(request.POST, request.FILES,instance=spending)
        print(form.is_valid())
        if form.is_valid():
            form.save()
        return HttpResponseRedirect("/")

def delete(request,id):
    Expense.objects.filter(id=id).delete()
    return HttpResponseRedirect("/")





