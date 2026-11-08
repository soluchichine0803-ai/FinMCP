from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .models import Transaction 
from django.db import transaction
from Accounts.models import Account
from .serializers import TransactionSerializer
# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_transfer(request):
    serializer = TransactionSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    from_account = serializer.validated_data['from_account']
    to_account = serializer.validated_data['to_account']
    amount = serializer.validated_data['amount']

    if from_account.owner_id != request.user.id:
        return Response(
            {'error': 'You do not own the source account.'},
            status=status.HTTP_403_FORBIDDEN
        )

    if from_account.pk == to_account.pk:
        return Response(
            {'error': 'Source and destination accounts must be different.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if amount <= 0:
        return Response(
            {'error': 'Transfer amount must be positive.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    with transaction.atomic():
        locked_accounts = Account.objects.select_for_update().filter(
            pk__in=[from_account.pk, to_account.pk]
        ).order_by('pk')

        accounts = {account.pk: account for account in locked_accounts}

        from_account = accounts.get(from_account.pk)
        to_account = accounts.get(to_account.pk)

        if from_account is None or to_account is None:
            return Response(
                {'error': 'Source or destination account no longer exists.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if from_account.owner_id != request.user.id:
            return Response(
                {'error': 'You do not own the source account.'},
                status=status.HTTP_403_FORBIDDEN
            )

        if from_account.balance < amount:
            return Response(
                {'error': 'Insufficient funds.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        from_account.balance -= amount
        to_account.balance += amount

        from_account.save(update_fields=['balance'])
        to_account.save(update_fields=['balance'])

        transfer = serializer.save(
            from_account=from_account,
            to_account=to_account
        )

    return Response(
        TransactionSerializer(transfer).data,
        status=status.HTTP_201_CREATED
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_transactions(request):
    transactions = Transaction.objects.filter(
        Q(from_account__owner=request.user) |
        Q(to_account__owner=request.user)
    ).order_by('-timestamp')

    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_transaction(request, tid):
    transaction = get_object_or_404(
        Transaction.objects.filter(
            Q(from_account__owner=request.user) |
            Q(to_account__owner=request.user)
        ),
        tid=tid
    )

    serializer = TransactionSerializer(transaction)
    return Response(serializer.data)
