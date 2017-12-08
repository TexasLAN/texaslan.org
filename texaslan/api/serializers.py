from django.contrib.auth import update_session_auth_hash

from rest_framework import serializers

from ..users.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(white_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'full_name', 'nick_name', 'phone_number', 'graduation_date', 'gender',
            'lan_class', 'active_semesters')

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        print('validation method')
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(
                    "Passwords must match"
                )
        return data


