from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.decorators import action
from .serializers import *


class ArticlesViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    # permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def create(self, request, *args, **kwargs):
        category_id = Category.objects.filter(admin_category=True).values('id')
        list_id = []
        for i in category_id:
            list_id.append(i['id'])

        if not int(request.data['category']) in list_id or request.user.is_superuser:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response({'Ваша статья отправлена на модерацию'})
        return Response({'Нельзя добавить статью'})


    def retrieve(self, request, pk=None):
        article = Article.objects.get(pk=pk)
        return Response ({
            'result': ArticleWithCommentsSerializer(article).data
        })


class CommentsViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    #permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'Ваш комментарий отправлен на модерацию'})

    def destroy(self, request, pk=None):
        try:
            comment = Comment.objects.get(pk=pk)
        except:
            Response ({}, status=404)

        if not request.user.is_superuser:
            if comment.author != request.user:
                return Response({}, status=403)

        comment.delete()
        return Response({'Комментарий успешно удален'})

    @action(detail=False, methods=['get'], url_path='my')
    def get_comment_user(self, request):
        comments = Comment.objects.filter(author=request.user)
        return Response({
            'result': CommentSerializer(comments, many=True).data
        })

class CategoriesViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    queryset = Category.objects.filter(sub_category=None)
    serializer_class = CategorySerializer


class SubCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly, )
    queryset = Category.objects.exclude(sub_category=None)
    serializer_class = SubCategorySerializer