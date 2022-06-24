import imp
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions, status
from django.db.models import Q

from product.models import Product as ProductModel
from product.serializers import ProductSerializer

from datetime import datetime

class ProductView(APIView):
    def get(self, request):
        user = request.user
        today = datetime.now()
        products = ProductModel.objects.filter(
            Q(user = user) |
            Q(exposed_end__gte=today,) &
            Q(is_active=True)
        )

        serialized_data = ProductSerializer(products,many=True).data
        return Response(serialized_data, status=status.HTTP_200_OK)
        

    def post(self, request):
        data = request.data.copy() 
        request.data._mutable=True 
        data["user"] = request.user.id 
        
        # request.data['user'] = request.user.id
        # print( request.data['user'] )
        product_serializer = ProductSerializer(data=data)

        if product_serializer.is_valid():  #request.data의 유효성을 검증 (True or False)
           product_serializer.save()
           return Response(product_serializer.data, status=status.HTTP_200_OK)

        #false일때
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, product_id):
        product = ProductModel.objects.get(id=product_id)
        product_serializer = ProductSerializer(product, data=request.data, partial=True)

        if product_serializer.is_valid():  #request.data의 유효성을 검증 (True or False)
           product_serializer.save()
           return Response(product_serializer.data, status=status.HTTP_200_OK)

        #false일때
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)