from rest_framework import serializers

from product.models import Product as ProductModel
from product.models import Review as ReviewModel

from datetime import datetime, timedelta
from django.db.models import Q



class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewModel   #어떤 모델을 쓸지 지칭
        fields = ["user", "product", "content", "rate", "registered_date", 
                 ]


class ProductSerializer(serializers.ModelSerializer):
    # review_set = ReviewSerializer(many=True, read_only=True)
    last_review = serializers.SerializerMethodField()
    def get_last_review(self, obj):
        # review_list = []
        # for review in obj.review_set.all():
        #     if review :
        #         review_list.append(review.content)
        #     print(review_list)
        #     print(review)
        # print(review_list[-1])

            # review_list.append(a)
        
        return {}
        # for review in obj.review_set.all():
        #     print(review)
        #     review_list.append(review)
        #     print("리스트", review_list)
        #     return str(review_list[-1])


    def validate(self, data):
        exposed_end_date = str(data.get("exposed_end",""))
        today = datetime.today().strftime('%Y-%m-%d')

        if exposed_end_date < today:
            raise serializers.ValidationError(
                detail={"error":"상품 노출이 종료되었습니다."}
            )
        return data

    def get(self, serialized_data):
        return serialized_data


    def create(self, validated_data):
        # product object 생성
        product = ProductModel(**validated_data)
        desc = validated_data.pop("desc")
        print(validated_data)
        product.save()

        today = datetime.today().strftime('%Y-%m-%d')
        end_msg = f'{today}에 등록된 상품입니다.'
        product.desc = product.desc + '\n' + end_msg 
        product.save()

        return product


    def update(self, instance, validated_data):
        # instance에는 입력된 object가 담긴다.
        # desc = validated_data.pop("desc")

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        today = datetime.today().strftime('%Y-%m-%d')
        str_msg = f'{today}에 수정된 상품입니다.'
        instance.desc = str_msg  + '\n' + instance.desc  
        instance.save()
        

        return instance


    class Meta:
        model = ProductModel   #어떤 모델을 쓸지 지칭
        fields = ["title", "user", "thumbnail", "desc", "registered_date", 
                 "exposed_end", "last_review", "price", "updated_date", "is_active"] 