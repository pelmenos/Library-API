from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'phone_number', 'address', 'registration_date', 'is_staff', 'password'
        ]
        read_only_fields = ['id', 'registration_date']
        write_only_fields = ['password']
