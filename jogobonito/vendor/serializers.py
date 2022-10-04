from dataclasses import field, fields
from pyexpat import model
from unicodedata import category
from rest_framework import serializers
from .models import Category, City, District,SubCategory,Turf, TurfSlot,Vendor,VendorOrder
from accounts.serializers import RegisterSerializer

class VendorRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
        extra_kwargs ={
            'password':{'write_only':True},
            'confirm_password':{'write_only':True}
        }

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name','slug','description','cat_image','id']


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'
        

class TurfSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    district = DistrictSerializer(many=False)
    city = CitySerializer(many=False)
    class Meta:
    
        model = Turf
        fields = '__all__'
        #['turf_name','slug','size','description','price','image','image1','image2','image3','id']
        #,'category','SubCategory','district','city','is_available'


class SlotSerializer(serializers.ModelSerializer):
    vendor = VendorRegisterSerializer(many=False)
    user = RegisterSerializer(many=False)
    turf = TurfSerializer(many=False)
    class Meta:
        model = TurfSlot
        fields = '__all__'


class TurfEditSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    district = DistrictSerializer(many=False)
    city = CitySerializer(many=False)
    class Meta:
        model = Turf
        fields = ['turf_name','slug','size','description','price','image','image1','image2','image3','SubCategory','category','district','city','is_available']

class SlotEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = TurfSlot
        fields = ['Date','Time','turf','is_available','Slot_No']


class VendorEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['first_name','last_name','phone_number']


class VendorchangepasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['confirm_password','password']



class VendorOrderSerializer(serializers.ModelSerializer):
    order_date = serializers.DateTimeField(format="%d %B %Y %I:%M %p")

    class Meta:
        model = VendorOrder
        fields = '__all__'
        depth = 2