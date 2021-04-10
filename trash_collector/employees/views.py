from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from .models import Employee


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
        return render(request, 'employees/index.html')


def match_zipcodes(request):
    Customer = apps.get_model('customers.customer')
    customers = Customer.objects.all()
    for customer in customers:
        print(customer.zipcode)
