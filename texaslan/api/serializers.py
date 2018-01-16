from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from ..users.models import User
from ..events.models import Event
import datetime

class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'start_time', 'end_time',  'title', 'location', 'description', 'creator' )

    def create(self, validated_data):
        return Event.objects.create(
                    start_time=validated_data.get('start_time'),
                    end_time=validated_data.get('end_time'),
                    title=validated_data.get('title'),
                    location=validated_data.get('location'),
                    description=validated_data.get('description'),
                    creator=validated_data.get('creator'),
                )

    def validate(self, data):
        user = data.get('creator')
        if not user.is_officer():
            raise serializers.ValidationError(
                    "Not authorized to create events"
                )
        return data

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'full_name', 'graduation_date', 'concentration',
            'confirm_password', 'password', 'email', 'username')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        password = validated_data.get('password', None)
        confirm_password = validated_data.get('confirm_password', None)

        if password and password == confirm_password:
            instance.set_password(password)

        instance.save()
        return instance

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(
                    "Passwords must match"
                )
        if self._username_is_taken(data['username']):
            raise serializers.ValidationError(
                    "Username is taken"
                )
        if self._email_is_taken(data['email']):
            raise serializers.ValidationError(
                    "Email is taken"
                )
        return data

    def _username_is_taken(self, username):
        users = User.objects.filter(username=username)
        return len(users) >= 1

    def _email_is_taken(self, email):
        users = User.objects.filter(email=email)
        return len(users) >= 1


