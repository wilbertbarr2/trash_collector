from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from .models import Employee
from datetime import timedelta, date, datetime

import js2py


# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.
from django.urls import reverse
from django.contrib.auth.models import Group


def index(request):
    # Get the employee model from the other app, it can now be used to query the db
    Customer = apps.get_model('customers.customer')
    customers = Customer.objects.all()
    for customer in customers:
        print(customer.zipcode)
    context = {
        'end': False
    }

    return render(request, 'employees/index.html', context)

def map(request):

    return render(request, 'employees/map.html')

def zipcode(request):
    if request.method == 'POST':
        user = request.user
        zipcode = request.POST.get('zipcode')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user.first_name = first_name
        user.last_name = last_name
        user.is_employee = 1
        user.manages_zipcode = 'This user is an employee and manages a zipcode'
        user.save()
        employee = Employee()
        employee.name = user.first_name + " " + user.last_name
        employee.zipcode = zipcode
        employee.user = user
        user.is_employee = 1
        employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        user = request.user
        employee = Employee.objects.get(user_id=user.id)
        context = {
            'employee': employee
        }
        return render(request, 'employees/index.html', context)


## Great job Rob on figuring out how to do this compare_days function!


def compare_days(customers):
    customerz = []
    x = datetime.now()

    for customer in customers:
        if x.strftime("%A") == customer.pickup_day:

            if customer.tem_suspend_start is not None:
                boolean = suspend_check(customer.tem_suspend_start.strftime("%Y-%m-%d"), customer.tem_suspend_end.strftime("%Y-%m-%d"))
                if boolean == True:
                    continue
                if boolean == False:
                    pass
            if customer.balance < 100:
                customerz.append(customer)
        if customer.onetime_pickup is not None:
            boolean = check_one_time_pickup(customer.onetime_pickup.strftime("%Y-%m-%d"))
            if boolean == True:
                if customer.balance < 100:
                    customerz.append(customer)
            if boolean == False:
                pass

    return customerz

## great job Rob on the time functions

def check_one_time_pickup(customer_onetime_pickup):
    x = datetime.now()
    today_check = x.strftime("%Y-%m-%d")
    if today_check == customer_onetime_pickup:
        return True
    else:
        return False

def suspend_check(start_date, end_date):
    x = datetime.now()
    x = x.strftime("%Y-%m-%d")
    today_check = datetime.strptime(x, "%Y-%m-%d")
    start = datetime.strptime(start_date, "%Y-%m-%d")
    stop = datetime.strptime(end_date, "%Y-%m-%d")
    while start < stop:
        if start == today_check:
            return True
        start = start + timedelta(days=1)
    return False


def charge_customer(request, customer_id):
    Customer = apps.get_model('customers.customer')
    customers = Customer.objects.all()
    x = datetime.now()
    picked_up = x.strftime("%Y-%m-%d")
    for customer in customers:
        if customer.id == customer_id:
            customer.last_pickup_date = picked_up
            customer.balance += 3
            customer.save()
            return match_zipcodes(request)
    return match_zipcodes(request)


def match_zipcodes(request):
    user = request.user
    employee = Employee.objects.get(user_id=user.id)
    Customer = apps.get_model('customers.customer')
    customers = Customer.objects.all()
    same_zipcode = []
    x = datetime.now()
    prevent_double_charge = x.strftime("%Y-%m-%d")
    for customer in customers:
        if customer.zipcode == employee.zipcode:
            if customer.last_pickup_date is None:
                same_zipcode.append(customer)
            if customer.last_pickup_date is not None:
                last_pickup = customer.last_pickup_date.strftime("%Y-%m-%d")
                if last_pickup != prevent_double_charge:
                    same_zipcode.append(customer)

    same_zipcode = compare_days(same_zipcode)
    if len(same_zipcode) < 1:
        context = {
            'end': True
        }
        return render(request, 'employees/index.html', context)
    context = {
        'customers': same_zipcode
    }
    return render(request, 'employees/index.html', context)


def daily_view(request):
    if request.method == 'POST':
        Customer = apps.get_model('customers.customer')
        customers = Customer.objects.all()
        day = request.POST.get('day')
        other_day = []
        for customer in customers:
            if customer.pickup_day == day:
                other_day.append(customer)
        context = {
            'customers': other_day
        }
        return render(request, 'employees/daily_view.html', context)

    else:
        return render(request, 'employees/daily_view.html')
