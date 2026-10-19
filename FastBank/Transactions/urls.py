from django.urls import path
import views


urlpatterns = [
    path('', views.get_transactions, name='get_transactions'),
    path('<int:tid>/', views.get_transaction, name='get_transaction'),
]