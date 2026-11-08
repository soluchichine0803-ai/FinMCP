from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_accounts, name='get_accounts'),
    path('create/', views.create_account, name='create_account'),
    path('<int:pk>/', views.account_detail, name='account_detail'),
]