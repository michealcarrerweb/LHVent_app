from account.conf import settings
from account.models import Account
from django.contrib.auth.models import User
from rest_framework import serializers


class PasswordSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Account
        fields = (
        	'spouse_name',
        	'street_address',
        	'city',
        	'state',
        	'zip_code',
        	'main_phone',
        	'alt_phone',        	
        )


class AccountSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Account
        fields = (
        	'spouse_name',
        	'street_address',
        	'city',
        	'state',
        	'zip_code',
        	'main_phone',
        	'alt_phone',        	
        )

class UserSerializer(serializers.HyperlinkedModelSerializer):

    account = AccountSerializer()

    class Meta:
        model = User
        fields = (
        	'url',
        	'username',
        	'first_name',        	    	 
        	'last_name',
        	'email',
        	'account',
        )

    def create(self, validated_data):
        account_data = validated_data.pop('account', None)
        user = super(UserSerializer, self).create(validated_data)
        self.update_or_create_profile(user, account_data)
        return user

    def update(self, instance, validated_data):
        account_data = validated_data.pop('account', None)
        self.update_or_create_profile(instance, account_data)
        return super(UserSerializer, self).update(instance, validated_data)

    def update_or_create_profile(self, user, account_data):
        # This always creates a Account if the User is missing one;
        # change the logic here if that's not right for your app
        Account.objects.update_or_create(user=user, defaults=account_data)
