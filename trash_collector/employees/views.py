from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps

# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.
from django.urls import reverse


def index(request):
    # Get the Customer model from the other app, it can now be used to query the db
    Customer = apps.get_model('customers.Customer')
    return render(request, 'employees/index.html')


def zipcode(request):
    if request.method == 'POST':
        user = request.user
        zipcode = request.POST.get('zipcode')
        user.zipcode = zipcode
        user.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        return render(request, 'employees/index.html')
