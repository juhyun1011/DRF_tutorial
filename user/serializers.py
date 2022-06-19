from rest_framework import serializers

from user.models import User as UserModel
from user.models import UserProfile as UserProfileModel
from user.models import Hobby as HobbyModel
from blog.models import Article as ArticleModel
from blog.models import Comment as CommentModel


class HobbySerializer(serializers.ModelSerializer):
    same_hobby_users = serializers.SerializerMethodField()
    def get_same_hobby_users(self, obj):
        # obj : hobby model의 object

        user_list = []
        for user_profile in obj.userprofile_set.all():
            user_list.append(user_profile.user.username)
        return user_list

        # return [user_profile.user.username for user_profile in obj.userprofile_set.all()]

    class Meta:
        model = HobbyModel 
        fields = ["name", "same_hobby_users"]


class UserProfileSerializer(serializers.ModelSerializer):
    hobby = HobbySerializer(many=True) #input data가 queryset일 경우 many=True

    class Meta:
        model = UserProfileModel  
        fields = ["introduction", "birthday", "age", "hobby"]


######
class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentModel
        fields = "__all__"


class AricleSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleModel
        fields = "__all__"

###########

class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()
    article_set = AricleSerializer(many=True)
    comment_set = CommentSerializer(many=True)


    class Meta:
        model = UserModel  
        fields = ["username", "email", "fullname", "join_date", "userprofile", "article_set", "comment_set"]   #리스트로 어떤 필드를 리턴해줄지 지정


