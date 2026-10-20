
from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.get_users, name='admin-users'),
    path('users/create/', views.create_user, name='admin-create-user'),
    path('users/<int:user_id>/', views.get_user, name='admin-user-detail'),
    path(
        'users/<int:user_id>/accounts/',
        views.get_user_accounts,
        name='admin-user-accounts'
    ),

    path('accounts/', views.get_accounts, name='admin-accounts'),
    path('accounts/<int:account_id>/', views.get_account, name='admin-account-detail'),
    path(
        'accounts/<int:account_id>/transactions/',
        views.get_account_transactions,
        name='admin-account-transactions'
    ),

    path('transactions/', views.get_transactions, name='admin-transactions'),
    path('transaction/<uuid:tid>/', views.get_transaction, name='admin-transaction-detail'),
]
