from rest_framework.decorators import api_view,authentication_classes
import datetime
from django.contrib import auth
from .authentication import create_access_token,create_refresh_token, JWTAuthentication,decode_refresh_token
from rest_framework import status,exceptions
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from .models import Account, UserToken
from .serializers import RegisterSerializer
from .verify import send,check
from rest_framework import viewsets
from django.contrib.auth import  authenticate

# Create your views here.
# email verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.shortcuts import render
from vendor.models import TurfSlot
from vendor.serializers import SlotSerializer
from payments.models import Order
from payments.serializers import OrderSerializer
@api_view(['POST'])
def registeruser(request):
    data = request.data
    print(data)
    try:
        print('rajaaaa')
        user = Account.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone_number=data['phone_number'],
            username=data['first_name']+'  '+data['last_name'],
            password=make_password(data['password'])
        )
        print('gdddhg')
        phone_number=data['phone_number']
        request.session['phone_number']=phone_number
        send(phone_number)

        serializer = RegisterSerializer(user,many=False)
        return Response(serializer.data)
    except :
        message = {'detail':'User with this email already exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def VerifyOtp(request):
    try:
        data=request.data
        phone_number=data['phone_number']
        code=data['code']
        if check(phone_number,code):
            print('hello')
            user = Account.objects.get(phone_number=phone_number)   
            print(user)       
            user.is_active= True
            user.save()
            serializer = RegisterSerializer(user, many=False)
            return Response(serializer.data)
        else:
            message = {'detail':'otp is not valid'}
               
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    except:
        message = {'detail':'somthin whent worng'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = Account.objects.filter(email=email).first()

        if user is None:
            response = Response()
           
            response.data={
                'message':'Invalid email'
            }
            return response        
            raise exceptions.AuthenticationFailed('Invalid email')

        if not user.check_password(password):
            response = Response()
           
            response.data={
                'message':'invalid password'
            }
            return response        
            raise exceptions.AuthenticationFailed('Invalid password')

        user = auth.authenticate(email=email, password=password)
        if user:
            access_token = create_access_token(user.id)
            refresh_token = create_refresh_token(user.id)

            UserToken.objects.create(
                user_id=user.id,
                token=refresh_token,
                expired_at=datetime.datetime.utcnow() + datetime.timedelta(days=7)
            )

            response = Response()
            
            response.set_cookie(key='refresh_token',value=refresh_token,httponly=True)
            response.data = {
                'token': access_token,
                'admin': user.is_admin,
                
            }
            return response
        else:
            response = Response()
            response.data={
                'message':'Not verifyde'
            }
            return response  

class UserAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    def get(self,request):
        return Response(RegisterSerializer(request.user).data)

class RefreshAPIView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        id = decode_refresh_token(refresh_token)

        if not  UserToken.objects.filter(
            user_id=id,
            token=refresh_token,
            expired_at__gt=datetime.datetime.now(tz=datetime.timezone.utc)
        ).exists():
            raise exceptions.AuthenticationFailed('unauthenticated')

        access_token = create_access_token(id)

        return Response({
            'token':access_token
        })

class LogoutAPIView(APIView):
    def post(self, request):
        refresh_token=request.COOKIES.get('refresh_token')
        UserToken.objects.filter(token=refresh_token).delete()
        
        response = Response()
        response.delete_cookie(key='refresh_token')
        response.data={
            'message':'logout'
        }
        return response        


@api_view(['POST'])
def forgotpassword(request):
    data=request.data
    email=data['email']
    if Account.objects.filter(email=email).exists():
        print(email)
        user = Account.objects.get(email=email)
        print(user)
        
        #reset password email
        current_site = get_current_site(request)
        mail_subject = 'pleace activate your account'
        message = render_to_string('accounts/forgotpassword.html', {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        to_email = email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

        message = {'detail':'email has sent succesfuly'}
        return Response(message, status=status.HTTP_200_OK)
    else:
        message = {'detail':'Account doses not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    


def resetpassword_validate(request,uidb64,token):
    if request.method=='POST':
        try:            
            uid = urlsafe_base64_decode(uidb64).decode()
            user = Account._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
            user = None
        
        if user is not None and default_token_generator.check_token(user,token):
            request.session['uid'] = uid
            print('succcess')
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']

            if password == confirm_password:
                print('passwords same')
                uid = request.session.get('uid')
                user = Account.objects.get(pk=uid)
                user.set_password(password)
                user.save()
                return render(request,'accounts/password_success.html')
     
        else:
            message={'detail':'link expired'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
    else:
        print('no')
        return render(request,'accounts/reset_password.html')


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def userchangepassword(request):
    data = request.data
    user=request.user
    print(user,'user')
    current_password =data['current_password']
    new_password = data['new_password']
    confirm_password = data['confirm_password']
    user = Account.objects.get(email=request.user)
    if new_password == confirm_password:
        if Account(email=user, password=current_password):
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
            message={'detail':'password reset successfully'}
            return Response(message,status=status.HTTP_200_OK)
        else:
            message={'detail':'plece enter valid current password'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)

    else:
        message={'detail':'password are not match'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def BookSlot(request,id):
    try:
        book = TurfSlot.objects.get(id=id)
        book.user=request.user
        book.is_available=False
        book.save()

        serializer = SlotSerializer(book,many=False)
        message = {'detail':'Slot posted Successfuly'}
        return Response(serializer.data)
    except:
        message = {'detail':'something weong!'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([JWTAuthentication])
class AllUserViewset(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = RegisterSerializer

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def GetUserOrder(request):
    try:
        user = request.user
        slot = TurfSlot.objects.filter(user=user,Is_booked=True)
        print(slot)
        order = Order.objects.filter(slot__in=slot)
        print(order)
        serializer = OrderSerializer(order,many=True)
        return Response(serializer.data)
    except:
        message = {'detail':'Slot is not available'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST) 


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def GetUserSingleOrder(request,id):
    try:
        user = request.user 
        slot = TurfSlot.objects.filter(user=user,Is_booked=True)
        print(slot)
        order = Order.objects.get(id=id)
        print(order)
        serializer = OrderSerializer(order,many=False)
        return Response(serializer.data)
    except:
        message = {'detail':'Slot is not available'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST) 