from rest_framework import serializers
from .models import Categorie, Article, Commentaire
from django.contrib.auth import get_user_model

User = get_user_model()

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ('id', 'nom', 'slug')


class ArticleListSerializer(serializers.ModelSerializer):
    categorie = CategorieSerializer(read_only=True)
    auteur = serializers.StringRelatedField(read_only=True)
    extrait = serializers.ReadOnlyField()

    class Meta:
        model = Article
        fields = ('id', 'titre', 'slug', 'extrait', 'image', 'categorie', 'auteur', 'date_creation', 'statut', 'meta_description', 'mots_cles')


class ArticleDetailSerializer(serializers.ModelSerializer):
    categorie = CategorieSerializer(read_only=True)
    auteur = serializers.StringRelatedField(read_only=True)
    commentaires = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('id', 'titre', 'slug', 'contenu', 'image', 'categorie', 'auteur', 'date_creation', 'date_modification', 'statut', 'meta_description', 'mots_cles', 'commentaires')

    def get_commentaires(self, obj):
        commentaires = obj.commentaires.filter(valide=True, parent__isnull=True).order_by('-date_creation')
        return CommentaireSerializer(commentaires, many=True).data


class ArticleCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('titre', 'contenu', 'image', 'categorie', 'statut', 'meta_description', 'mots_cles')

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, "user"):
            validated_data['auteur'] = request.user
        return super().create(validated_data)


class CommentaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentaire
        fields = ('id', 'article', 'auteur', 'auteur_user', 'contenu', 'date_creation', 'valide', 'parent')
        read_only_fields = ('date_creation', 'valide', 'auteur_user')

    def validate(self, attrs):
        # simple anti-spam: contenu min length
        contenu = attrs.get('contenu', '')
        if len(contenu.strip()) < 5:
            raise serializers.ValidationError("Le commentaire est trop court.")
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['auteur_user'] = request.user
            validated_data['auteur'] = request.user.get_full_name() or request.user.username
        # par défaut, commentaire non validé (modération)
        validated_data['valide'] = False
        return super().create(validated_data)
