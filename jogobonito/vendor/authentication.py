import jwt,datetime
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication,get_authorization_header
from .models import Vendor
from rest_framework.response import Response
from rest_framework import status, exceptions,generics





def create_access_token(id):
    return jwt.encode({
          #payload
          'user_id':id ,
          'exp': datetime.datetime.utcnow() +datetime.timedelta(days=1),
          'iat':datetime.datetime.utcnow()
    },'access_secret',algorithm='HS256')

def create_refresh_token(id):
    return jwt.encode({
          #payload
          'user_id':id ,
          'exp': datetime.datetime.utcnow()+datetime.timedelta(days=7),
          'iat':datetime.datetime.utcnow()
    },'refresh_secret',algorithm='HS256')



def decode_access_token (token):
      try:
        payload = jwt.decode(token,'access_secret',algorithms='HS256')
        print(payload['user_id'],"jjj")
        return payload ['user_id']
      except Exception as e: 
        print (e,"decode_access_token")
        raise exceptions.AuthenticationFailed('unauthenticated')

def decode_refresh_token (token):
      try:
        payload = jwt.decode(token,'refresh_secret',algorithms='HS256')
        return payload ['user_id']
      except : 
        raise exceptions.AuthenticationFailed('unauthenticated')

# MIDDLEWARE

class VendorAuthentication(BaseAuthentication):
      def authenticate(self, request):
            auth = get_authorization_header(request).split()

            if auth and len(auth) == 2:
                  token = auth[1].decode('utf-8')
                  id = decode_access_token(token)
                  # print(id)
                  vendor = Vendor.objects.get(pk=id)
                  # print(vendor)
                  if vendor.is_Vendor:
                        return (vendor, None)
                  
            raise exceptions.AuthenticationFailed('unauthenticated')
          




# class StaffAuthentication(BaseAuthentication):
#         def authenticate(self, request):

#               auth = get_authorization_header(request).split()
#               print(auth,"ook")

#               if auth and len(auth) == 2:
#                     token = auth[1].decode('utf-8')
#                     print(token,"yes")
#                     id =decode_access_token(token)
#                     print(id)
#                     vendor = Vendor.objects.get(pk=id)
#                     print("rasa")
#                     if vendor.is_Vendor:
#                         return (vendor,None)

                    
#               raise exceptions.AuthenticationFailed('unauthenticated')