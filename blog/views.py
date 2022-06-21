from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from blog.models import Article as ArticleModel
from DRF_tutorial.permissions import IsAdminandIsSevendaysOrIsAuthenticatedReadOnly
from datetime import datetime

# from user.serializers import ArticleSerializer
from blog.serializers import ArticleSerializer


# Create your views here.

class ArticleView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [IsAdminandIsSevendaysOrIsAuthenticatedReadOnly]

    def get(self, request):
        # user = request.user
        today = datetime.now()
        articles = ArticleModel.objects.filter(
            exposed_start__lte=today,
            exposed_end__gte=today
        ).order_by("id")

        return Response(ArticleSerializer(articles, many=True).data)



    def post(self, request):
        user = request.user
        request.data['author'] = user.id
        article_serializer = ArticleSerializer(data=request.data)

        if article_serializer.is_valid():  #request.data의 유효성을 검증 (True or False)
            article_serializer.save()
            return Response(article_serializer.data, status=status.HTTP_200_OK)

        #false일때
        return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        # title  = request.data.get('title')
        # category = request.data.get('category')
        # content = request.data.get('content')
        # user = request.user
       
        # print(title)

        # if len(title) <= 5 :
        #     return Response({"error":"타이틀은 5자 이상 작성해주세요."}, status=status.HTTP_400_BAD_REQUEST)   #status=400과 동일
        # if len(content) <= 20 :
        #     return Response({"error":"내용은 20자 이상 작성해주세요."}, status=status.HTTP_400_BAD_REQUEST) 
        # if not category :
        #     return Response({"error":"카테고리를 지정해주세요."}, status=status.HTTP_400_BAD_REQUEST) 

        # article = ArticleModel(
        #     title = title,
        #     content=content,
        #     author = user
        # )

        # article.save()
        # article.category.add(*category)

        # return Response({"message":"게시글 작성 성공!"})

   

