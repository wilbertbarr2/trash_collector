from django.urls import path

from . import views

# TODO: Determine what distinct pages are required for the customer user stories, add a path for each in urlpatterns

app_name = "customers"
urlpatterns = [
    path('', views.index, name="index"),
    path('customer', views.trash_customer, name='trash_customer'),
    path('suspend', views.suspend_account, name='suspend_account'),
    path('request/<int:customer_id>', views.request_cancel, name="request_cancel")
]
