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
    with transaction.atomic():
        serializer = TransactionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        from_account_id = serializer.validated_data['from_account'].id
        to_account_id = serializer.validated_data['to_account'].id
        amount = serializer.validated_data['amount']

        # Prevent transfers to the same account
        if from_account_id == to_account_id:
            return Response(
                {"error": "Cannot transfer to the same account"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Lock accounts in a consistent order
        accounts = Account.objects.select_for_update().filter(
            id__in=[from_account_id, to_account_id]
        ).order_by('id')

        accounts = {account.id: account for account in accounts}

        if len(accounts) != 2:
            return Response(
                {"error": "One or both accounts not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        from_account = accounts[from_account_id]
        to_account = accounts[to_account_id]

        # Validate amount
        if amount <= 0:
            return Response(
                {"error": "Amount must be greater than zero"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check sufficient balance
        if from_account.balance < amount:
            return Response(
                {"error": "Insufficient balance"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Perform transfer
        from_account.balance -= amount
        to_account.balance += amount

        from_account.save(update_fields=['balance'])
        to_account.save(update_fields=['balance'])

        # Save transaction record using the verified accounts
        serializer.save(
            from_account=from_account,
            to_account=to_account
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    with transaction.atomic():#makes db ops all or nothing
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            from_account_id = serializer.validated_data['from_account'].id
            to_account_id = serializer.validated_data['to_account'].id
            amount = serializer.validated_data['amount']

            #check if accounts exists
            try:
                # Fetch the accounts from the database
                from_account = Account.objects.select_for_update().get(id=from_account_id)
                to_account = Account.objects.select_for_update().get(id=to_account_id)
            except Account.DoesNotExist:
                return Response(
                    {"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)
       
            # Check if the from_account has sufficient balance
            if from_account.balance < amount:
                return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Perform the transfer
            from_account.balance -= amount
            to_account.balance += amount
            
            # Save the updated account balances
            from_account.save()
            to_account.save()
            
            # Save the transaction record
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
