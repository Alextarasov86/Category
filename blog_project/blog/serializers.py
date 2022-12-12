from rest_framework import serializers
from .models import *
from users.serializers import UserSerializer



class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        exclude = ('is_published',)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ('is_published',)


class ArticleWithCommentsSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    def get_comments(self, article):
        comments = Comment.objects.filter(article=article)
        return CommentSerializer(comments, many=True).data

    def get_author(self, article):
        return UserSerializer(article.author).data

    class Meta:
        model = Article
        fields = ('id', 'title', 'text', 'author', 'date_created', 'comments')

class CategorySerializer(serializers.ModelSerializer):
    articles = serializers.SerializerMethodField()

    def get_articles(self, category):
        articles = Article.objects.filter(category=category)
        return ArticleSerializer(articles, many=True).data

    class Meta:
        model = Category
        fields = ('id', 'title', 'articles')


class SubCategorySerializer(serializers.ModelSerializer):
    articles = serializers.SerializerMethodField()

    def get_articles(self, category):
        articles = Article.objects.filter(category=category)
        return ArticleSerializer(articles, many=True).data

    class Meta:
        model = Category
        fields = ('id', 'title', 'sub_category', 'articles')