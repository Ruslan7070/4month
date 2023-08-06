from django.urls import path
from products.views import *


urlpatterns = [
    path('products/', products_view),
    path('products/<int:id>/', detail_view),
    path('categories/', CategoriesView.as_view()),
    path('products/create/', ProductsCreateView.as_view()),
]
