
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from Accounts.models import Account
from Transactions.models import Transaction

from .serializers import (
    AdminUserSerializer,
    AdminUserCreateSerializer,
    AdminAccountSerializer,
    AdminTransactionSerializer,
)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_users(request):
    users = User.objects.all().order_by('id')
    serializer = AdminUserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    serializer = AdminUserSerializer(user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_user(request):
    serializer = AdminUserCreateSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        return Response(
            AdminUserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_user_accounts(request, user_id):
    user = get_object_or_404(User, id=user_id)
    accounts = Account.objects.filter(owner=user).order_by('id')
    serializer = AdminAccountSerializer(accounts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_accounts(request):
    accounts = Account.objects.all().order_by('id')
    serializer = AdminAccountSerializer(accounts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_account(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    serializer = AdminAccountSerializer(account)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_account_transactions(request, account_id):
    account = get_object_or_404(Account, id=account_id)

    transactions = Transaction.objects.filter(
        Q(from_account=account) | Q(to_account=account)
    ).order_by('-timestamp')

    serializer = AdminTransactionSerializer(transactions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_transactions(request):
    transactions = Transaction.objects.all().order_by('-timestamp')
    serializer = AdminTransactionSerializer(transactions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_transaction(request, tid):
    transaction = get_object_or_404(Transaction, tid=tid)
    serializer = AdminTransactionSerializer(transaction)
    return Response(serializer.data)
