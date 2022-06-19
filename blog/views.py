from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from blog.models import Article as ArticleModel
from DRF_tutorial.permissions import RegistedMoreThanthreedays


# Create your views here.

class ArticleView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [RegistedMoreThanthreedays]

    def post(self, request):
        title  = request.data.get('title')
        category = request.data.get('category')
        content = request.data.get('content')
        user = request.user
       
        print(title)

        if len(str(title)) <= 5 :
            return Response({"error":"게시글을 작성할 수 없습니다."})   
        if len(str(content)) <= 20 :
            return Response({"error":"게시글을 작성할 수 없습니다."}) 
        if category is None :
            return Response({"error":"카테고리를 지정해주세요."}) 

        article = ArticleModel(
            title = title,
            content=content,
            author = user
        )

        article.save()
        article.category.add(*category)

        return Response({"message":"게시글 작성 성공!"})

    def get(self, request):
        user = request.user

        articles = ArticleModel.objects.filter(author=user)
        titles = [article.title for article in articles]

        return Response({'article_list': titles})

