from account.conf import settings
from account.models import Account
from django.contrib.auth.models import User
from rest_framework import serializers


# class AccountSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Account
#         fields = (
        	
#         	'initial_password', 
#         	'spouse_name',
#         	'street_address',
#         	'city',
#         	'state',
#         	'zip_code',
#         	'main_phone',
#         	'alt_phone',
        	
#         )


# class UserSerializer(serializers.ModelSerializer):

#     account = AccountSerializer()

#     class Meta:
#         model = User
#         fields = (
        	
#         	'username',
#         	'first_name',        	    	 
#         	'last_name',
#         	'email',
#         	'account',
#         )

#     def create(self, validated_data):
#         print(validated_data)
#         account_data = validated_data.pop('account')
#         print(account_data)
#         print(validated_data)
#         account = Account.objects.create(**account_data)
#         user = User.objects.create(account=account, **validated_data)
#         print(user.username, user.first_name, user.last_name, user.id, user.email)
        
#         return account

class AccountSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Account
        fields = (
        	# 'url',
        	# 'initial_password', 
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
        	# 'pk',
        	'username',
        	'first_name',        	    	 
        	'last_name',
        	'email',
        	# 'id',
        	'account',
        )

    # def create(self, validated_data):
    #     account_data = validated_data.pop('account')
    #     user = User.objects.create(**validated_data)
    #     Account.objects.create(user=user, **account_data)       
    #     return user

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
        # This always creates a Profile if the User is missing one;
        # change the logic here if that's not right for your app
        Account.objects.update_or_create(user=user, defaults=account_data)

    # def create(self, validated_data):
    #     profile_data = validated_data.pop('profile', None)
    #     user = super(UserSerializer, self).create(validated_data)
    #     self.update_or_create_profile(user, profile_data)
    #     return user

    # def update(self, instance, validated_data):
    #     profile_data = validated_data.pop('profile', None)
    #     self.update_or_create_profile(instance, profile_data)
    #     return super(UserSerializer, self).update(instance, validated_data)

    # def update_or_create_profile(self, user, profile_data):
    #     # This always creates a Profile if the User is missing one;
    #     # change the logic here if that's not right for your app
    #     Profile.objects.update_or_create(user=user, defaults=profile_data)
                    ##############
# class TrackSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Track
#         fields = ('order', 'title', 'duration')

# class AlbumSerializer(serializers.ModelSerializer):
#     tracks = TrackSerializer(many=True)

#     class Meta:
#         model = Album
#         fields = ('album_name', 'artist', 'tracks')

#     def create(self, validated_data):
#         tracks_data = validated_data.pop('tracks')
#         album = Album.objects.create(**validated_data)
#         for track_data in tracks_data:
#             Track.objects.create(album=album, **track_data)
#         return album
###########
# class Verb(models.Model):#User
#     verb = models.TextField()
#     verbal_noun = models.TextField()
#     verbal_adjective = models.TextField()
#     present = models.TextField()
#     future = models.TextField()
#     habitual_present = models.TextField()
#     conditional = models.TextField()
#     past_habitual = models.TextField()
#     past_subjunctive = models.TextField()
#     present_subjunctive = models.TextField()
#     imperative = models.TextField()

# class Past(models.Model):#Account
#     verb = models.OneToOneField(Verb)
#     first_singular = models.TextField()
#     second_singular = models.TextField()
#     third_singular = models.TextField()

# from rest_framework import serializers
# from conjugations.models import Verb, Past

# class PastSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Past#Accou
#         fields = ('first_singular','second_singular','third_singular')

# class VerbSerializer(serializers.ModelSerializer):
#     past = PastSerializer()

#     class Meta:
#         model = Verb#User
#         fields = ('verb','verbal_noun','verbal_adjective','past','present',
#                 'future','habitual_present','conditional','past_habitual',
#                 'past_subjunctive','present_subjunctive','imperative')

#     def create(self, validated_data):
#         past_data = validated_data.pop('past')
#         verb = Verb.objects.create(**validated_data)
#         Past.objects.create(verb=verb, **past_data)
#         return verb















    # def update(self, instance, validated_data):
    #     profile_data = validated_data.pop('profile')
    #     # Unless the application properly enforces that this field is
    #     # always set, the follow could raise a `DoesNotExist`, which
    #     # would need to be handled.
    #     profile = instance.profile

    #     instance.username = validated_data.get('username', instance.username)
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.save()

    #     profile.is_premium_member = profile_data.get(
    #         'is_premium_member',
    #         profile.is_premium_member
    #     )
    #     profile.has_support_contract = profile_data.get(
    #         'has_support_contract',
    #         profile.has_support_contract
    #      )
    #     profile.save()

    #     return instance

    # def create(self, validated_data):
    #     profile_data = validated_data.pop('profile')
    #     user = User.objects.create(**validated_data)
    #     Profile.objects.create(user=user, **profile_data)
    #     return user

    # def update(self, instance, validated_data):
    #     profile_data = validated_data.pop('profile')
    #     # Unless the application properly enforces that this field is
    #     # always set, the follow could raise a `DoesNotExist`, which
    #     # would need to be handled.
    #     profile = instance.profile

    #     instance.username = validated_data.get('username', instance.username)
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.save()

    #     profile.is_premium_member = profile_data.get(
    #         'is_premium_member',
    #         profile.is_premium_member
    #     )
    #     profile.has_support_contract = profile_data.get(
    #         'has_support_contract',
    #         profile.has_support_contract
    #      )
    #     profile.save()

    #     return instance
