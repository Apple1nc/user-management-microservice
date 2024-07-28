from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True,required=False)
    password2 = serializers.CharField(write_only=True,required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'username', 'role', 'password1','password2']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': False},  # Allow email to be optional
        }

    def validate(self, data):
        password1 = data.get('password1')
        password2 = data.get('password2')

        if password1 != password2:
            raise serializers.ValidationError("Passwords do not match.")
        return data
    

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            role=validated_data['role'],
            password=validated_data['password1']
        )
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.role = validated_data.get('role', instance.role)

        password = validated_data.get('password1')
        if password:
            instance.set_password(password)

        instance.save()
        return instance
