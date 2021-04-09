from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, reverse
from .models import Customer


# Create your views here.

# TODO: Create a function for each path created in customers/urls.py. Each will need a template as well.


def index(request):
    # get the logged in user within any view function
    user = request.user
    # This will be useful while creating a customer to assign the logged in user as the user foreign key
    # Will also be useful in any function that needs
    print(user)
    return render(request, 'customers/index.html')


def trash_customer(request):
    if request.method == 'POST':
        user = request.user
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')

        user.first_name = first_name
        user.last_name = last_name

        user.save()
        customer = Customer()
        customer.user_id = user.id
        customer.name = user.first_name + " " + user.last_name
        return HttpResponseRedirect(reverse('customers:index'))
    else:
        return render(request, 'customers/trash_customer.html')


def suspend_account(request):
    if request.method == 'POST':
        user = request.user
        user.is_active = 0
        user.save()
        return HttpResponseRedirect(reverse('customers:index'))
    else:
        return render(request, 'customers/suspend_account.html')

