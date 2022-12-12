from django.urls import path, include
from .views import *
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'articles', ArticlesViewSet)
router.register(r'comments', CommentsViewSet)
router.register(r'categories', CategoriesViewSet, basename='categories')
router.register(r'subcategories', SubCategoryViewSet, basename='sub')
urlpatterns = [
    path('', include(router.urls)),
]