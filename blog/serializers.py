from unicodedata import category
from rest_framework import serializers

from user.models import User as UserModel
from user.models import UserProfile as UserProfileModel
from user.models import Hobby as HobbyModel
from blog.models import Category as CategoryModel
from blog.models import Article as ArticleModel
from blog.models import Comment as CommentModel



class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryModel  
        fields = ["name"]

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.author.username

    class Meta:
        model = CommentModel  
        fields = ["author", "content"]

class ArticleSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    comment = CommentSerializer(many=True, source="comment_set", read_only=True)

    def get_category(self, obj):
        return [category.name for category in obj.category.all()]

    class Meta:
        model = ArticleModel  
        fields = ["author", "category", "title", "content", "comment",
                "exposed_start", "exposed_end"]

        extra_kwargs = {
            'title': {
                # error_messages : 에러 메세지를 자유롭게 설정 할 수 있다.
                'error_messages': {
                    # required : 값이 입력되지 않았을 때 보여지는 메세지
                    'required': '제목이 입력되지 않았습니다.',
                    },
                    # required : validator에서 해당 값의 필요 여부를 판단한다.
                    'required': False # default : True
                    },
            }