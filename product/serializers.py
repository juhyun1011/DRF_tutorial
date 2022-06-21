from rest_framework import serializers

from product.models import Product as ProductModel


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductModel   #어떤 모델을 쓸지 지칭
        fields = ["title", "author", "thumbnail", "desc", "registered_date", 
                "exposed_start", "exposed_end"]