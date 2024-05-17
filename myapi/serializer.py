from rest_framework import serializers
from .models import *



class Usersignuperializer(serializers.ModelSerializer):
    class Meta:
        model = UserManagement
        fields = ["username","email","password"]
  


class Loginseralizer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class Leavemangementserializer(serializers.ModelSerializer):
    class Meta:
        model = Leavemanagement
        fields = '__all__'
        depth=1

class Leaveserializer(serializers.ModelSerializer):
    class Meta:
        model = Leavemanagement
        fields = '__all__'


class Alluserserializer(serializers.ModelSerializer):
    class Meta:
        model = UserManagement
        fields = ["id","username","email"]
  