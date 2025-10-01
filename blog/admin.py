from django.contrib import admin
from .models import Categorie, Article, Commentaire

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'slug')
    prepopulated_fields = {"slug": ("nom",)}
    search_fields = ('nom',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'auteur', 'statut', 'date_creation')
    list_filter = ('statut', 'categorie', 'date_creation')
    search_fields = ('titre', 'contenu', 'meta_description', 'mots_cles')
    prepopulated_fields = {"slug": ("titre",)}
    readonly_fields = ('date_creation', 'date_modification')
    fieldsets = (
        (None, {'fields': ('titre', 'slug', 'categorie', 'auteur', 'statut')}),
        ('Contenu', {'fields': ('contenu', 'image')}),
        ('SEO', {'fields': ('meta_description', 'mots_cles')}),
        ('Dates', {'fields': ('date_creation', 'date_modification')}),
    )


@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('auteur', 'article', 'valide', 'date_creation')
    list_filter = ('valide', 'date_creation')
    search_fields = ('auteur', 'contenu', 'article__titre')
    actions = ['valider_commentaires']

    def valider_commentaires(self, request, queryset):
        updated = queryset.update(valide=True)
        self.message_user(request, f"{updated} commentaire(s) validé(s).")
    valider_commentaires.short_description = "Valider les commentaires sélectionnés"
