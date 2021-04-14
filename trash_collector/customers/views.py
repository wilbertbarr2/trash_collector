from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404
from .models import Customer


# Create your views here.

# TODO: Create a function for each path created in customers/urls.py. Each will need a template as well.


def index(request):
    # get the logged in user within any view function
    user = request.user
    # This will be useful while creating a customer to assign the logged in user as the user foreign key
    customers = Customer.objects.all()
    for customer in customers:
        if customer.user_id == user.id:
            context = {
                'customer': customer
            }
            return render(request, 'customers/index.html', context)

    # Will also be useful in any function that needs
    print(user)
    return render(request, 'customers/index.html')


def trash_customer(request):
    if request.method == 'POST':
        user = request.user
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        zipcode = request.POST.get('zipcode')
        state = request.POST.get('state')
        city = request.POST.get('city')
        pickup_day = request.POST.get('pickup_day')
        user.email = request.POST.get('email')
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        try:
            customer = Customer.objects.get(user_id=user.id)
        except:
            customer = Customer()
            customer.name = user.first_name + " " + user.last_name
            customer.zipcode = zipcode
            customer.address = address
            customer.state = state
            customer.city = city
            customer.pickup_day = pickup_day
            customer.user = user
            customer.save()
            return HttpResponseRedirect(reverse('customers:index'))

        customer.name = user.first_name + " " + user.last_name
        customer.zipcode = zipcode
        customer.address = address
        customer.state = state
        customer.city = city
        customer.pickup_day = pickup_day
        customer.user_id = user.id
        customer.save()
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
        user = request.user
        customer = Customer.objects.get(user_id=user.id)
        context = {
            'customer': customer
        }
        return render(request, 'customers/suspend_account.html', context)

## the customer_id parameter, I dont think I ended up using. I just haven't found time yet to go through code
## pretty sure I dont need it... just going to save it till later to fix it in the url.py and .html pages.


def request_cancel(request, customer_id):
    user = request.user
    customer = Customer.objects.get(user_id=user.id)
    if request.method == 'POST':
        one_time = request.POST.get('one_time')
        extra_service = request.POST.get('extra_service')
        start = request.POST.get('start')
        end = request.POST.get('end')
        if one_time is not None:
            customer.has_used_one_time_extra_service = True
            customer.onetime_pickup = one_time
        if extra_service is not None:
            customer.onetime_pickup = extra_service
            customer.balance += 20
        customer.tem_suspend_start = start
        customer.tem_suspend_end = end
        customer.save()

        return HttpResponseRedirect(reverse('customers:index'))
    else:
        customer = Customer.objects.get(user_id=user.id)
        context = {
            'customer': customer
        }
        return render(request, 'customers/request_cancel.html', context)



