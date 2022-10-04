from dataclasses import field, fields
from pyexpat import model
from rest_framework import serializers
from .models import Account

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        #['first_name','last_name','email','phone_number','password','username','is_active']
        extra_kwargs ={
            'password':{'write_only':True}
        }

class VerifyOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['is_active']