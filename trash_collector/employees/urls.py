from django.urls import path

from . import views

# TODO: Determine what distinct pages are required for the customer user stories, add a path for each in urlpatterns

app_name = "employees"
urlpatterns = [
    path('', views.index, name="index"),
    path('zip', views.zipcode, name="zipcode"),
    path('hello', views.match_zipcodes, name="match_zip"),
    path('charge/<int:customer_id>', views.charge_customer, name="charge_customer")
]
