from rest_framework import serializers

from user.models import User as UserModel
from user.models import UserProfile as UserProfileModel
from user.models import Hobby as HobbyModel

from blog.serializers import ArticleSerializer


class HobbySerializer(serializers.ModelSerializer):
    same_hobby_users = serializers.SerializerMethodField()
    def get_same_hobby_users(self, obj):
        # obj : hobby model의 object
        # user= self.context["request"].user
        user_list = []
        for user_profile in obj.userprofile_set.all():
            user_list.append(user_profile.user.username)
        return user_list

        # return [user_profile.user.username for user_profile in obj.userprofile_set.exclude(user=user)]

    class Meta:
        model = HobbyModel 
        fields = ["name", "same_hobby_users"]


class UserProfileSerializer(serializers.ModelSerializer):
    hobby = HobbySerializer(many=True, read_only=True) #input data가 queryset일 경우 many=True
    get_hobbys = serializers.ListField(required=False)

    class Meta:
        model = UserProfileModel  
        fields = ["introduction", "birthday", "age", "hobby", "get_hobbys"]



class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()
    articles = ArticleSerializer(many=True, source="article_set", read_only=True)

    def validate(self, data):
        if not data.get("email","").endswith("@naver.com"):
            raise serializers.ValidationError(
                detail={"error":"네이버 메일만 가입할 수 있습니다."}
            )
        return data


    #기존 함수를 덮어씀
    def create(self, validated_data):
        user_profile = validated_data.pop("userprofile")
        get_hobbys = user_profile.pop("get_hobbys", [])
        password = validated_data.pop("password")
        


        # User object 생성
        user = UserModel(**validated_data)
        user.set_password(password)
        user.save()

        # UserProfile object 생성
        user_profile = UserProfileModel.objects.create(user=user, **user_profile)

         # hobby 등록
        user_profile.hobby.add(*get_hobbys)
        user_profile.save()

        return user


    def update(self, instance, validated_data):
        # instance에는 입력된 object가 담긴다.
        user_profile = validated_data.pop("userprofile")
        get_hobbys = user_profile.pop("get_hobbys", [])

        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
                continue
            
            setattr(instance, key, value)
        instance.save()

        user_profile_object = instance.userprofile
        for key, value in user_profile.items():
            setattr(user_profile_object, key, value)
        
        instance.save()

        return instance


    class Meta:
        model = UserModel  
        fields = ["username","password", "email", "fullname", "join_date", "userprofile", "articles"]   #리스트로 어떤 필드를 리턴해줄지 지정

        extra_kwargs = {
                # write_only : 해당 필드를 쓰기 전용으로 만들어 준다.
                # 쓰기 전용으로 설정 된 필드는 직렬화 된 데이터에서 보여지지 않는다.
                'password': {'write_only': True}, # default : False
                'email': {
                    # error_messages : 에러 메세지를 자유롭게 설정 할 수 있다.
                    'error_messages': {
                        # required : 값이 입력되지 않았을 때 보여지는 메세지
                        'required': '이메일을 입력해주세요.',
                        # invalid : 값의 포맷이 맞지 않을 때 보여지는 메세지
                        'invalid': '알맞은 형식의 이메일을 입력해주세요.'
                        },
                        # required : validator에서 해당 값의 필요 여부를 판단한다.
                        'required': False # default : True
                        },
                }

    

   