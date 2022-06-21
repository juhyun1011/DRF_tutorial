from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions, status
from product.models import Product as ProductModel

from product.serializers import ProductSerializer

class ProductView(APIView):
    def get(self, request):
        user = request.user
        products = ProductModel.objects.filter(author=user)
        return Response(ProductSerializer(products, many=True).data, status=status.HTTP_200_OK)


    def post(self, request):
        product_serializer = ProductSerializer(data=request.data)

        if product_serializer.is_valid():  #request.data의 유효성을 검증 (True or False)
            product_serializer.save()
            return Response(product_serializer.data, status=status.HTTP_200_OK)

        #false일때
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)