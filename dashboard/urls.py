from django.urls import path

from . import views





urlpatterns = [
    path("", views.index, name="index"),
    path("add-customer/", views.add_customer, name="add_customer"),
    path("get-customers/", views.get_customer_data, name="get_customers"),
    path("delete/<int:id>/", views.delete_customer, name="delete_customers"),
    path("update/<int:id>/", views.update_customer, name="update_customers"),
    path("get-item-count", views.get_item_count, name="get_item_count"),
    path("download_file", views.download_file, name="download_file"),
     
]
