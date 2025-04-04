from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.get_all_prodect,name="products"),
    path("products/<str:pk>/", views.get_by_id,name="get_by_id"),
    path("product/filter/", views.get_all_prodect_filters,name="get_all_prodect_filters"),
    path("product/Pagenation/", views.get_all_prodect_Pagenation,name="get_all_prodect_Pagenation"),
    
    
    
]
