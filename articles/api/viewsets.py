from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from ..models import Article
from .serializers import ArticleSerializer,ArticleDetailSeriazlizer
from .permissions import IsArticleAuthor
from rest_framework.response import Response
 
class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    permission_classes = [IsArticleAuthor]

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleSerializer
        return ArticleDetailSeriazlizer
    
    @action(methods=['get'],detail=False)
    def liked(self,request):
        queryset = request.user.liked_articles
        serializer = self.get_serializer(queryset,many=True)
        return Response(serializer.data)