from rest_framework import viewsets, generics, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .models import Categorie, Article, Commentaire
from .serializers import (
    CategorieSerializer, ArticleListSerializer, ArticleDetailSerializer,
    ArticleCreateUpdateSerializer, CommentaireSerializer
)

class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [IsAdminUser]  # création/modif/suppression admin seulement

    def get_permissions(self):
        # GET list/detail allowed to everyone, but write actions limited
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().select_related('categorie', 'auteur')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categorie__slug', 'statut']
    search_fields = ['titre', 'contenu', 'meta_description', 'mots_cles']
    ordering_fields = ['date_creation', 'date_modification']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['list']:
            return ArticleListSerializer
        if self.action in ['retrieve']:
            return ArticleDetailSerializer
        return ArticleCreateUpdateSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        # par défaut, ne montrer que les articles publiés pour les utilisateurs non-admin
        user = getattr(self.request, 'user', None)
        if not (user and user.is_staff):
            qs = qs.filter(statut='published')
        return qs

    def perform_create(self, serializer):
        serializer.save(auteur=self.request.user)

    @action(detail=True, methods=['get'], url_path='by-slug', url_name='by-slug')
    def by_slug(self, request, pk=None):
        # optional helper if you want /articles/<slug>/by-slug/
        article = get_object_or_404(Article, slug=pk)
        serializer = ArticleDetailSerializer(article, context={'request': request})
        return Response(serializer.data)


class CommentaireViewSet(viewsets.ModelViewSet):
    queryset = Commentaire.objects.select_related('article', 'auteur_user').all()
    serializer_class = CommentaireSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['article', 'valide']
    search_fields = ['auteur', 'contenu']
    ordering_fields = ['date_creation']

    def get_queryset(self):
        qs = super().get_queryset()
        user = getattr(self.request, 'user', None)
        # if not admin, only show validated comments
        if not (user and user.is_staff):
            qs = qs.filter(valide=True)
        return qs

    def perform_create(self, serializer):
        serializer.save()
