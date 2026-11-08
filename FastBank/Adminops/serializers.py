
from django.contrib.auth.models import User
from rest_framework import serializers

from Accounts.models import Account
from Transactions.models import Transaction


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'date_joined']


class AdminUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class AdminAccountSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(
        source='owner.username',
        read_only=True
    )

    class Meta:
        model = Account
        fields = [
            'id',
            'owner_username',
            'account_number',
            'balance',
            'currency',
            'status',
        ]


class AdminTransactionSerializer(serializers.ModelSerializer):
    from_account_number = serializers.CharField(
        source='from_account.account_number',
        read_only=True
    )
    to_account_number = serializers.CharField(
        source='to_account.account_number',
        read_only=True
    )

    class Meta:
        model = Transaction
        fields = [
            'id',
            'tid',
            'from_account_number',
            'to_account_number',
            'amount',
            'status',
            'timestamp',
        ]
