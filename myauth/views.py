from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from income.forms import IncomeForm
from category.forms import CategoryForm
from expenses.forms import ExpensesForm
from category.models import Category
from expenses.models import Expenses
from income.models import Income
from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Sum
import datetime

# Create your views here.
def signin(request):
    if request.method=='GET':
        return render(request,'signin.html')
    else:
        u=request.POST.get("username")
        p=request.POST.get("password")
        user=authenticate(username=u,password=p)
        if user is not None:
            login(request,user)
            return redirect('dashboard')
        return render(request,'signin.html',{'errmsg':'your username or password is incorrect'})

def signup(request):
    if request.method=='GET':
        context = {
            'form':UserCreationForm()
        }

        return render(request,'signup.html',context)
    else:
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request,'signup.html',{'form':form})
@login_required(login_url='login')
def dashboard(request):
    data = sum_by_category(request.user.id)
    evs=expensesvssaving(request.user.id)
    context={
        'data':data,
        'evs': evs
    }
    return render(request,'dashboard.html',context)

@login_required(login_url='login')
def income(request):
    if request.method=='GET':

        context = {
            'form':IncomeForm(),
            'income':Income.objects.filter(user_id=request.user.id,date__month=MyCurrentMonth(),date__year=MyCurrentYear()),
            'total':Income.objects.filter(user_id=request.user.id,date__month=MyCurrentMonth(),date__year=MyCurrentYear()).aggregate(Sum('rupees')),
            'prevInc': Income.objects.filter(user_id=request.user.id, date__month=MyPreviousMonth(),date__year=MyPreviousMonthYear()),
            'prevTotal': Income.objects.filter(user_id=request.user.id, date__month=MyPreviousMonth(),date__year=MyPreviousMonthYear()).aggregate(Sum('rupees'))
        }
        return render(request,'income.html',context)
    else:
        form=IncomeForm(request.POST)
        if form.is_valid():
            data=form.save(commit=False)
            data.user_id = request.user.id
            data.save()
            return redirect('income')
        return render(request,'income.html',{'form':form})

@login_required(login_url='login')
def expenses(request):
    if request.method=='GET':
        context ={
            'form':ExpensesForm(request.user),
            'expenses':Expenses.objects.filter(user_id=request.user.id,date__month=MyCurrentMonth(),date__year=MyCurrentYear()),
            'total': Expenses.objects.filter(user_id=request.user.id, date__month=MyCurrentMonth(),date__year=MyCurrentYear()).aggregate(Sum('rupees')),
            'prevExp':Expenses.objects.filter(user_id=request.user.id,date__month=MyPreviousMonth(),date__year=MyPreviousMonthYear()),
            'prevTotal':Expenses.objects.filter(user_id=request.user.id, date__month=MyPreviousMonth(),date__year=MyPreviousMonthYear()).aggregate(Sum('rupees'))
           # 'prevTotal':getPreviousMonth(request.user.id).aggregate(Sum('rupees'))
        }
        return render(request,'expenses.html',context)
    else:
        form=ExpensesForm(request.user,request.POST,request.FILES or None)
        if form.is_valid():
            data=form.save(commit=False)
            data.user_id=request.user.id
            data.save()
            return redirect('expenses')
        return render(request,'expenses.html',{'form':form})

@login_required(login_url='login')
def category(request):
    if request.method=='GET':
        context ={
            'form':CategoryForm(),
            'cat':Category.objects.filter(user_id=request.user.id)
        }
        return render(request,'category.html',context)
    else:
        form=CategoryForm(request.POST)
        if form.is_valid():
            data=form.save(commit=False)
            data.user_id=request.user.id
            data.save()
            return redirect('category')
        return render(request,'category.html',{'form':form})

def mylogout(request):
    logout(request)
    return redirect('login')

def MyCurrentMonth():
    return datetime.date.today().month

def MyCurrentYear():
    return datetime.date.today().year

def MyPreviousMonth():
    today_month = datetime.date.today().month

    if today_month!=1:
        previous_month=today_month-1
    else:
        previous_month=12
    return previous_month


def MyPreviousMonthYear():
    today_month = datetime.date.today().month
    today_year = datetime.date.today().year

    if today_month != 1:
        previous_month_year = today_year
    else:
        previous_month_year = today_year - 1
    return previous_month_year


# def getPreviousMonth(id):
#     today_month=datetime.date.today().month
#     today_year=datetime.date.today().year
#
#     if today_month!=1:
#         previous_month=today_month-1
#         previous_month_year=today_year
#     else:
#         previous_month=12
#         previous_month_year=today_year-1
#     return Expenses.objects.filter(user_id=id,date__month=previous_month,date__year=previous_month_year)

def expenses_edit(request,id):
    data=Expenses.objects.get(pk=id)
    form=ExpensesForm(request.user,request.POST or None,request.FILES or None,instance=data)
    if form.is_valid():
        form.save()
        return redirect('expenses')
    context={
        'form':form
    }
    return render(request,'expenses_edit.html',context)

def expenses_delete(request,id):
    exp= Expenses.objects.get(pk=id)
    exp.delete()
    return redirect('expenses')

def sum_by_category(id):
    all_category = Category.objects.filter(user_id=id)
    category_label=[]
    category_sum=[]
    for c in all_category:
        t=Expenses.objects.filter(user_id=id,date__month=MyCurrentMonth(),date__year=MyCurrentYear(),category_id=c.id).aggregate(Sum('rupees'))
        print(t)
        if t['rupees__sum'] is not None:
            category_sum.append(t['rupees__sum'])
        else:
            category_sum.append(0)
        category_label.append(c.title)
    return list(zip(category_label,category_sum))


def income_edit(request,id):
    data = Income.objects.get(id=id)
    form = IncomeForm(request.POST or None, request.FILES or None, instance=data)
    if form.is_valid():
        form.save()
        return redirect('income')
    context={
        'form':form
    }
    return render(request,'income_edit.html',context)

def income_delete(request,id):
    inc = Income.objects.get(id=id)
    inc.delete()
    return redirect('income')

def expensesvssaving(id):
    income=Income.objects.filter(user_id=id,date__month=MyCurrentMonth(),date__year=MyCurrentYear()).aggregate(Sum('rupees'))
    total_income=income['rupees__sum']
    if total_income is None:
        total_income=0
    expenses=Expenses.objects.filter(user_id=id,date__month=MyCurrentMonth(),date__year=MyCurrentYear()).aggregate(Sum('rupees'))
    total_expenses=expenses['rupees__sum']
    if total_expenses is None:
        total_expenses=0
    saving=total_income-total_expenses
    return list(zip(['Expenses','saving'],[total_expenses,saving]))