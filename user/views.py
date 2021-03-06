from functools import partial
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from django.contrib.auth import login, logout, authenticate

from django.db.models import F

from user.serializers import UserSerializer
from user.models import User as UserModel


class UserView(APIView): 
    permission_classes = [permissions.IsAuthenticated] # 로그인 된 사용자만 view 조회 가능

    #역참조를 활용해 나와 같은 취미를 가진 사람 찾기
    #one-to-one field는 예외로 _set이 붙지 않는다.
    def get(self, request):
        return Response(UserSerializer(request.user, context={"request": request}).data, status=status.HTTP_200_OK)
       
    #회원가입
    def post(self, request):
        user_serializer= UserSerializer(data=request.data, context={"request": request})

        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #회원 정보 수정
    def put(self, request, obj_id):
        # user= request.user
        user = UserModel.objects.get(id=obj_id)
        user_serializer = UserSerializer(user, data=request.data, partial= True) #user도 같이 넣어줘야함. 어떤 걸 수정할건지.

        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #회원 탈퇴
    def delete(self, request):
        return Response({'message': 'delete method!!'})

class UserApiView(APIView):
    permission_classes = [permissions.AllowAny]

    #로그인
    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        user = authenticate(request, username=username, password=password)

        if not user:
            return Response({"error":"존재하지 않는 계정이거나 패스워드가 일치하지 않습니다."})
            
        login(request, user)
        return Response({"message":"로그인 성공!"})

    #로그아웃
    def delete(self, request):
        logout(request)
        return Response({"message":"logout success!"})
