from django.urls import path
from order_structure.views import *

urlpatterns = [
    path('add_company/',register_company),
    path('companies_list/', companies_list),
    path('place_order/', order_placement),
    path('order_info/', order_book)
]
