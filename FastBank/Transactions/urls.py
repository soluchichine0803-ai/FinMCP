from django.urls import path

urlpatterns = [
    path('/', views.get_transactions, name='get_transactions'),
    path('/<int:id>/', views.get_transaction, name='get_transaction'),
]