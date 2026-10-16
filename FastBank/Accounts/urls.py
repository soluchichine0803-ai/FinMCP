from django.urls import pat
import views

urlpatterns = [
    path('/', views.get_accounts, name='get_accounts'),
    path('/<int:id>/', views.get_account, name='get_account'),
]