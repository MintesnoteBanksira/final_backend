from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'full_name', 'location', 'farm_size', 'coffee_type', 'last_farming_time', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            full_name=validated_data['full_name'],
            location=validated_data['location'],
            farm_size=validated_data['farm_size'],
            coffee_type=validated_data['coffee_type'],
            last_farming_time=validated_data['last_farming_time'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
