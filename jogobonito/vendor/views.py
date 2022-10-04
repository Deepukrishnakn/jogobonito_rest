import datetime
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.decorators import api_view,authentication_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from accounts.authentication import JWTAuthentication
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.shortcuts import render
from payments.serializers import OrderSerializer

import json
import razorpay
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes
from django.core.mail import send_mail
from .serializers import VendorOrderSerializer
from .models import VendorOrder
from django.conf import settings
from payments.models import Order

from .serializers import CitySerializer, DistrictSerializer, SlotEditSerializer, SlotSerializer, SubcategorySerializer, VendorRegisterSerializer,TurfSerializer,CategorySerializer
from django.contrib.auth.hashers import make_password
from .models import City, District, SubCategory, TurfSlot, VendorToken,Vendor,Turf,Category
from .authentication import create_access_token,create_refresh_token, VendorAuthentication
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import  authenticate

# Create your views here.

# class TurfViewPagination(LimitOffsetPagination):
#     default_limit = 1
#     max_limit = 12



@api_view(['POST'])
def vendorRegister(request):
    data = request.data
    print(data)
    try:
        print('its ok')
        vendor = Vendor.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone_number=data['phone_number'],
            password=make_password(data['password']),
            confirm_password=data['confirm_password'],
            turf_name=make_password(data['turf_name']),
            district=data['district'],
            city=data['city'],
            turf_address=data['turf_address'],
            description=data['description'],
            # image=data['image'],
        )

        send_mail('Hello  ',
                'Thank You For Join with Jogobonito ,Your Application is underprocess ',
                'deepukrishna25@gmail.com'
                ,[vendor.email]   
                ,fail_silently=False)
        serializer = VendorRegisterSerializer(vendor,many=False)
        message = {'detail':'vendor Registration send Successfuly'}
        return Response(serializer.data)
    except :
        message = {'detail':'vendor with this email already exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


class LoginVenndorView(APIView):
    def post(self,request):
        
        email = request.data['email']
        print(email)
       
        password = request.data['password']
        print(password)

        vendorz = Vendor.objects.filter(email=email).exists()
        #

        if  not vendorz :
            print('ddddd')
            response = Response()
            response.data={
                'message':'Email Inncorect'
            }
            return response 

        vendor = Vendor.objects.filter(email=email).first()
        passwords =vendor.password
        print(passwords,'jjjj')
        if  not check_password(password, passwords) :
            response = Response()
            response.data={
               'message':'Password Inncorect'
            }
            return response  

        # vendor = auth.authenticate(email=email, password=password)  
        print(vendor,'ddddd')
        if vendor.is_active:
            access_token = create_access_token(vendor.id)
            refresh_token = create_refresh_token(vendor.id)
            print("ooooo")
            VendorToken.objects.create(
                vendor_id = vendor.id,
                token= refresh_token,
                expired_at =  datetime.datetime.utcnow()+datetime.timedelta(seconds=7),
            )
            response = Response()
            response.set_cookie(key='refresh_token',value=refresh_token, httponly=True)
            response.data = {
                'token': access_token,
                # 'refreshToken': refresh_token,
            }
            return response   
        else:
            response = Response()
            response.data={
                'message':'Your Not a Vendor'
            }
            return response  

    
class VendorLogoutAPIView(APIView):
    def post(self, request):
        refresh_token=request.COOKIES.get('refresh_token')
        VendorToken.objects.filter(token=refresh_token).delete()
        response = Response()
        response.delete_cookie(key='refresh_token')
        response.data={
            'message':'logout'
        }
        return response        


class VendorAPIView(APIView):
    authentication_classes = [VendorAuthentication]
    def get(self, request):
        print('kittiyoo')
        user=request.user
        users=Vendor.objects.get(email=user.email)
        serializer=VendorRegisterSerializer(users,many=False)
        return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([VendorAuthentication])
def change_password(request):
    data = request.data
    user=request.user
    print(user,'user')
    current_password =data['current_password']
    new_password = data['new_password']
    confirm_password = data['confirm_password']
    user = Vendor.objects.get(email=request.user)
    if new_password == confirm_password:
        if authenticate(email=user, password=current_password):
            print('ok')
        else:
            print('not oke')
        success = user.check_password(current_password)

        if authenticate(email=request.user, password=current_password):
            print('ok')
        if success:
            user.set_password(new_password)
            user.save()
            #auth logout(request)
            message={'success':'plece enter valid current password'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
        else:
            message={'success':'plece enter valid current password'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)

    else:
        message={'success':'password reset successfully'}
        return Response(message,status=status.HTTP_200_OK)

    
    
@api_view(['POST'])
def resetPassword(request):
    data=request.data
    password =data['password']
    confirm_password =data['confirm_password']

    if password == confirm_password:
        uid =request.session.get('uid')
        print(uid)
        user=Vendor.objects.get(id=uid)
        user.set_password(password)
        user.save()
        message={'success':'plece enter valid current password'}
        return Response(message,status=status.HTTP_200_OK)

    else:
        message={'error':'password missmatch'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST)

# @api_view(['PATCH'])
# @authentication_classes([VendorAuthentication])
# def VendorEdit(request,id):
#     try:
#         user=Vendor.objects.get(id=id)
#         edit=VendorEditSerializer(instance=user,data=request.data)
#         if edit.is_valid():
#             edit.save()
#         return Response(edit.data)
#     except:
#         response=Response()
#         response.data={
#             'message':'somthing Wrong '
#         }
#         return response  

# vendor CRUD operations ............
class AllvendorViewset(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorRegisterSerializer


@api_view(['GET'])
def Turfs(request,category_slug):
    categories = None
    turf = None
    try:
        if category_slug is not None:
            categories=Category.objects.get(slug = category_slug)
            print(categories)
            turf = Turf.objects.filter(category=categories)
            serializer = TurfSerializer(turf ,many=True)
            return Response(serializer.data) 
        else:
            turf = Turf.objects.all()
            serializer = TurfSerializer(turf ,many=True)
            return Response(serializer.data) 

    except:
        turf = Turf.objects.all()
        message = {'detail':'Turf is not available'}

        return Response(message,status=status.HTTP_400_BAD_REQUEST) 


@api_view(['GET'])
def Turfs_District(request,id):
    try:        
        district=District.objects.get(id=id)
        print(district)
        job=Turf.objects.filter(district=district,is_available=True)
        serializer=TurfSerializer(job,many=True)
        return Response(serializer.data)
    except:
        turf = Turf.objects.all()
        message = {'detail':'Turf is not available'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST) 


@api_view(['GET'])
def Turfs_City(request,id):
    try:        
        city=City.objects.get(id=id)
        print(city)
        turf=Turf.objects.filter(city=city,is_available=True)
        serializer=TurfSerializer(turf,many=True)
        return Response(serializer.data)
    except:
        turf = Turf.objects.all()
        message = {'detail':'Turf is not available'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST) 


@api_view(['GET'])
def City_by_district(request,id):
    try:        
        district=District.objects.get(id=id)
        print(district)
        city=City.objects.filter(district=district)
        serializer=CitySerializer(city,many=True)
        return Response(serializer.data)
    except:
        city = City.objects.all()
        message = {'detail':'city is not available'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST) 


@api_view(['GET'])
def Subcate_by_Cate(request,id):
    try:        
        category=Category.objects.get(id=id)
        print(category)
        Subcate=City.objects.filter(category=category)
        serializer=SubcategorySerializer(Subcate,many=True)
        return Response(serializer.data)
    except:
        Subcate = SubCategory.objects.all()
        message = {'detail':'Subcategory is not available'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST) 


@api_view(['GET'])
def Turf_details(request,category_slug,turf_slug):
    try:
        single_turf = Turf.objects.get(category__slug=category_slug,slug=turf_slug)
        serializer = TurfSerializer(single_turf ,many=False)
        return Response(serializer.data) 
    except:
        message = {'detail':'Turf is not available'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST) 

@api_view(['GET'])
def TurfView(request):
    try:
        turf = Turf.objects.filter(is_available=True)
        serializer = TurfSerializer(turf ,many=True)
        return Response(serializer.data) 
    except:
        message = {'detail':'Turf is not available'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST) 
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SerchTurfViewSet(viewsets.ModelViewSet):
    queryset = Turf.objects.all().filter(is_available=True)
    serializer_class = TurfSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('slug','turf_name')
    search_fields = ('slug','turf_name','category__category_name','district__district','city__city','size')
    # pagination_class = TurfViewPagination



@api_view(['POST'])
@authentication_classes([VendorAuthentication])
def addTurf(request):

    data = request.data
    print(data)
    try:
        print('its add turf')
        print(request.user)
        turfs = Turf.objects.create(
            turf_name = request.data['turf_name'],
            slug = request.data['slug'],
            size = request.data['size'],
            description = request.data['description'],
            price = request.data['price'],
            image = request.FILES['image'],
            image1 = request.FILES['image1'],
            image2 = request.FILES['image2'],
            image3 = request.FILES['image3'],
            category_id = request.data['category'],
            SubCategory_id = request.data['SubCategory'],
            district_id = request.data['district'],
            city_id = request.data['city'],
            vendor = request.user,
            is_available = request.data['is_available']
        )

        serializer = TurfSerializer(turfs,many=False)
        message = {'detail':'turf posted Successfuly'}
        return Response(serializer.data)
    except :
        message = {'detail':'something weong!'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

                
class DistrictViewset(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


class CityViewset(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class SubcategoryViewset(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubcategorySerializer
    
@authentication_classes([VendorAuthentication])
class TurfViewset(viewsets.ModelViewSet):
    queryset = Turf.objects.all()
    serializer_class = TurfSerializer

@authentication_classes([VendorAuthentication])
class SlotallViewset(viewsets.ModelViewSet):
    queryset = TurfSlot.objects.all()
    serializer_class = SlotSerializer


@api_view(['POST'])
@authentication_classes([VendorAuthentication])
def addSlot(request):
    data = request.data
    print(data)
    try:
        print('its add slot')
        print(request.user)
        slots = TurfSlot.objects.create(
            Date = request.data['Date'],
            Time = request.data['Time'],
            Slot_No = request.data['Slot_No'],
            turf_id = request.data['turf_id'],
            is_available = request.data['is_available'],
            vendor = request.user
        )

        serializer = SlotSerializer(slots,many=False)
        message = {'detail':'Slot posted Successfuly'}
        return Response(serializer.data)
    except :
        message = {'detail':'something weong!'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def GetSlot(request,id):
    try:
        now = datetime.datetime.now()
        turf = Turf.objects.get(id=id)
        slot = TurfSlot.objects.filter(turf=turf,Date__gte=now,Time__gte=now,Is_booked=False)
        serializer = SlotSerializer(slot,many=True)
        return Response(serializer.data)
    except:
        message = {'detail':'Slot is not available'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST) 


# @api_view(['GET'])
# @authentication_classes([VendorAuthentication])
# def GetBookedSlot(request):
#     try:
#         vendor = request.user
#         slot = TurfSlot.objects.filter(vendor=vendor,Is_booked=True)
#         print(slot)
#         order = Order.objects.filter(slot__in=slot)
#         print(order)
#         serializer = SlotSerializer(slot,many=True)
#         return Response(serializer.data)
#     except:
#         message = {'detail':'Sloat is not available'}
#         return Response(message,status=status.HTTP_400_BAD_REQUEST) 

@api_view(['GET'])
@authentication_classes([VendorAuthentication])
def GetOrder(request):
    try:
        vendor = request.user
        slot = TurfSlot.objects.filter(vendor=vendor,Is_booked=True)
        print(slot)
        order = Order.objects.filter(slot__in=slot)
        print(order)
        serializer = OrderSerializer(order,many=True)
        return Response(serializer.data)
    except:
        message = {'detail':'Slot is not available'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST) 


@api_view(['GET'])
@authentication_classes([VendorAuthentication])
def GetSingleOrder(request,id):
    try:
        vendor = request.user
        slot = TurfSlot.objects.filter(vendor=vendor,Is_booked=True)
        print(slot)
        order = Order.objects.get(id=id)
        print(order)
        serializer = OrderSerializer(order,many=False)
        return Response(serializer.data)
    except:
        message = {'detail':'Slot is not available'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST) 


@api_view(['GET'])
@authentication_classes([VendorAuthentication])
def turf_view_by_vendor(request):
    try:
        vendor = request.user
        turf = Turf.objects.filter(vendor=vendor)
        serializer = TurfSerializer(turf,many=True)
        return Response(serializer.data)
    except:
        message = {'detail':'Slot is not available'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST) 


# @api_view(['PATCH'])
# @authentication_classes([VendorAuthentication])
# def editturf(request,id):
#     try:
#         turf=Turf.objects.get(id=id)
#         edit=TurfEditSerializer(instance=turf,data=request.data)
#         if edit.is_valid():
#             edit.save()
#         return Response(edit.data)
#     except:
#         response=Response()
#         response.data={
#             'message':'somthing Wrong '
#         }
#         return response  



@api_view(['PATCH'])
@authentication_classes([VendorAuthentication])
def editslot(request,id):
    try:
        slot=TurfSlot.objects.get(id=id)
        edit=SlotEditSerializer(instance=slot,data=request.data)
        if edit.is_valid():
            edit.save()
        return Response(edit.data)
    except:
        response=Response()
        response.data={
            'message':'somthing Wrong '
        }
        return response  


@api_view(['GET'])
@authentication_classes([VendorAuthentication])
def Get_all_Slot(request,id):
    try:
        turf = Turf.objects.get(id=id)
        slot = TurfSlot.objects.filter(turf=turf)
        serializer = SlotSerializer(slot,many=True)
        return Response(serializer.data)
    except:
        message = {'detail':'Slot is not available'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST) 

#payment................................

@api_view(['POST'])
# @authentication_classes([VendorAuthentication])
def start_payment(request):   
    amount = request.data['amount']
    name = request.data['name']  
    vendor = request.data['vendor'] 
    client = razorpay.Client(auth=(settings.RAZORPAY_ID,settings.RAZORPAY_KEY))

    # create razorpay order
    # the amount will come in 'paise' that means if we pass 50 amount will become
    # 0.5 rupees that means 50 paise so we have to convert it in rupees. So, we will 
    # mumtiply it by 100 so it will be 50 rupees.
    payment = client.order.create({"amount": int(amount) * 100, 
                                   "currency": "INR", 
                                   "payment_capture": "1"})

    # we are saving an order with isPaid=False because we've just initialized the order
    # we haven't received the money we will handle the payment succes in next 
    # function
    order = VendorOrder.objects.create(
                                 order_amount=amount, 
                                 order_payment_id=payment['id'],
                                 vendor_id=vendor,
                               )

    serializer = VendorOrderSerializer(order)

    """order response will be 
    {'id': 17, 
    'order_date': '23 January 2021 03:28 PM', 
    'order_product': '**product name from frontend**', 
    'order_amount': '**product amount from frontend**', 
    'order_payment_id': 'order_G3NhfSWWh5UfjQ', # it will be unique everytime
    'isPaid': False}"""

    data = {
        "payment": payment,
        "order": serializer.data
    }
    return Response(data)


@api_view(['POST'])
# @authentication_classes([VendorAuthentication])
def handle_payment_success(request):
    vendor_id = request.data['vendor'] 
    print(vendor_id)
    # request.data is coming from frontend
    # res = json.loads(request.data["response"])
    res = json.loads(request.data["response"])
    print(res,'response is hweww')

    """res will be:
    {'razorpay_payment_id': 'pay_G3NivgSZLx7I9e', 
    'razorpay_order_id': 'order_G3NhfSWWh5UfjQ', 
    'razorpay_signature': '76b2accbefde6cd2392b5fbf098ebcbd4cb4ef8b78d62aa5cce553b2014993c0'}
    this will come from frontend which we will use to validate and confirm the payment
    """

    ord_id = ""
    raz_pay_id = ""
    raz_signature = ""

    # res.keys() will give us list of keys in res
    for key in res.keys():
        if key == 'razorpay_order_id':
            ord_id = res[key]
        elif key == 'razorpay_payment_id':
            raz_pay_id = res[key]
        elif key == 'razorpay_signature':
            raz_signature = res[key]
    # get order by payment_id which we've created earlier with isPaid=False
    order = VendorOrder.objects.get(order_payment_id=ord_id)
    # we will pass this whole data in razorpay client to verify the payment
    data = {
        'razorpay_order_id': ord_id,
        'razorpay_payment_id': raz_pay_id,
        'razorpay_signature': raz_signature
    }
  
    client = razorpay.Client(auth=(settings.RAZORPAY_ID,settings.RAZORPAY_KEY))
   
    # checking if the transaction is valid or not by passing above data dictionary in 
    # razorpay client if it is "valid" then check will return None
    check = client.utility.verify_payment_signature(data)
    if check is None:
       
        return Response({'error': 'Something went wrong'})

    # if payment is successful that means check is None then we will turn isPaid=True
    vendor = Vendor.objects.get(id=vendor_id)
    print(vendor)
    vendor.is_Paid=True
    vendor.save()
    order.isPaid = True
    order.save()
    send_mail('Hello  ',
            'payment successfully received! ,Thank You For join with Jogobonito ,Your can check your profile',
            'deepukrishna25@gmail.com'
            ,[vendor.email]   
            ,fail_silently=False)

    data = {
        'message': 'payment successfully received!'
    }

    return Response(data)


    