from accounts.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self,data):
        user = authenticate(**data)
        if user:
            return user
        raise serializers.ValidateError('Incorrect Username or Password. Please revise your credentials')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email','username', 'password')
        #this is used in order to hash the passowrd
        extra_kwargs = {'password': {'write_only': True}}

        #calls the create_user method in account.managers model
    def create(self, validated_data):
        user = User.objects.create_user(
            name =validated_data["name"],
            username = validated_data["username"],
            email = validated_data["email"],
            password = validated_data["password"]
            )
        return user

#Retrieve user information when called. id, name, email and username is returned
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'username')
