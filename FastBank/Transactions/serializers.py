from rest_framework import serializers
from .models import Transaction
from Accounts.models import Account


class TransactionSerializer(serializers.ModelSerializer):
    from_account = serializers.SlugRelatedField(
        slug_field='account_number',
        queryset=Account.objects.all()
    )
    to_account = serializers.SlugRelatedField(
        slug_field='account_number',
        queryset=Account.objects.all()
    )

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['tid', 'status', 'timestamp']