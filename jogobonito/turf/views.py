
# import datetime
# from rest_framework import status,exceptions
# from rest_framework.decorators import api_view
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.contrib.auth.hashers import make_password

# from .serializers import CategorySerializer, TurfSerializer
# from .models import Category, Turf
# from rest_framework import viewsets
# # Create your views here.

# class TurfViewSet(viewsets.ModelViewSet):
#     queryset = Turf.objects.all()
#     serializer_class = TurfSerializer
#     def perform_create(self, serializer):
#         serializer.save()


# @api_view(['GET'])
# def category_view(request,slug):
#     category = Category.objects.all()
#     serializer = CategorySerializer(category, many=True)
#     return Response(serializer.data)
