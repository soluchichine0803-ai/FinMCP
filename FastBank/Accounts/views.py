
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Account
from .serializers import AccountSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_accounts(request):
    accounts = Account.objects.filter(owner=request.user)
    serializer = AccountSerializer(accounts, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def account_detail(request, pk):
    account = get_object_or_404(
        Account,
        pk=pk,
        owner=request.user
    )

    if request.method == 'GET':
        serializer = AccountSerializer(account)
        return Response(serializer.data)

    serializer = AccountSerializer(
        account,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_account(request):
    serializer = AccountSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )
