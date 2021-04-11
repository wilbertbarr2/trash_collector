from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from .models import Employee
import datetime
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

    return render(request, 'employees/index.html')


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


def match_zipcodes(request):
    user = request.user
    employee = Employee.objects.get(user_id=user.id)
    Customer = apps.get_model('customers.customer')
    customers = Customer.objects.all()
    same_zipcode = []
    for customer in customers:
        if customer.zipcode == employee.zipcode:
            same_zipcode.append(customer)
    same_zipcode = compare_days(customers)
    context = {
        'customers': same_zipcode
    }
    return render(request, 'employees/index.html', context)

## Great job Rob on figuring out how to do this compare_days function!


def compare_days(customers):
    customerz = []
    x = datetime.datetime.now()
    for customer in customers:
        if x.strftime("%A") == customer.pickup_day:
            customerz.append(customer)

    return customerz


def charge_customer(request, customer_id):
    Customer = apps.get_model('customers.customer')
    customers = Customer.objects.all()
    for customer in customers:
        if customer.id == customer_id:
            customer.balance += 10
            customer.save()
            return re_match_zipcodes(request, customer.id)
    return match_zipcodes(request)


def re_match_zipcodes(request, customer_id):
    user = request.user
    employee = Employee.objects.get(user_id=user.id)
    Customer = apps.get_model('customers.customer')
    customers = Customer.objects.all()
    same_zipcode = []
    for customer in customers:
        if customer.zipcode == employee.zipcode:
            same_zipcode.append(customer)
    same_zipcode = compare_days(customers)
    #for customer in same_zipcode:
    #    if customer.id == customer_id:
    #        same_zipcode.remove(customer)
    context = {
        'customers': same_zipcode
    }
    return render(request, 'employees/index.html', context)