from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategorieViewSet, ArticleViewSet, CommentaireViewSet

router = DefaultRouter()
router.register(r'categories', CategorieViewSet, basename='categorie')
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'commentaires', CommentaireViewSet, basename='commentaire')

urlpatterns = [
    path('api/', include(router.urls)),
]
