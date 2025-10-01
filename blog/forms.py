# blog/forms.py

from django import forms
from django.core.exceptions import ValidationError
from .models import Article, Commentaire, Categorie, Tag, AbonnementNewsletter
from django.contrib.auth.models import User


class ArticleForm(forms.ModelForm):
    """
    Formulaire pour la création et modification d'articles
    """
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text="Sélectionnez les tags pertinents pour cet article"
    )
    
    class Meta:
        model = Article
        fields = [
            'titre', 'sous_titre', 'resume', 'contenu', 'categorie', 'tags',
            'image_principale', 'image_alt', 'statut', 'type_article',
            'date_publication', 'meta_title', 'meta_description', 'meta_keywords',
            'epingle', 'commentaires_actifs', 'partage_reseaux'
        ]
        
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre de l\'article'
            }),
            'sous_titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sous-titre (optionnel)'
            }),
            'resume': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Résumé de l\'article (300 caractères max)'
            }),
            'contenu': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 15,
                'placeholder': 'Contenu de l\'article'
            }),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
            'image_alt': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Texte alternatif pour l\'image'
            }),
            'statut': forms.Select(attrs={'class': 'form-control'}),
            'type_article': forms.Select(attrs={'class': 'form-control'}),
            'date_publication': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre SEO (60 caractères max)'
            }),
            'meta_description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Description SEO (160 caractères max)'
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mots-clés SEO séparés par des virgules'
            }),
        }
    
    def clean_titre(self):
        titre = self.cleaned_data.get('titre')
        if len(titre) < 10:
            raise ValidationError('Le titre doit contenir au moins 10 caractères.')
        return titre
    
    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if len(resume) < 50:
            raise ValidationError('Le résumé doit contenir au moins 50 caractères.')
        if len(resume) > 300:
            raise ValidationError('Le résumé ne peut pas dépasser 300 caractères.')
        return resume
    
    def clean_contenu(self):
        contenu = self.cleaned_data.get('contenu')
        if len(contenu) < 200:
            raise ValidationError('Le contenu doit contenir au moins 200 caractères.')
        return contenu
    
    def clean_meta_title(self):
        meta_title = self.cleaned_data.get('meta_title')
        if meta_title and len(meta_title) > 60:
            raise ValidationError('Le titre SEO ne peut pas dépasser 60 caractères.')
        return meta_title
    
    def clean_meta_description(self):
        meta_description = self.cleaned_data.get('meta_description')
        if meta_description and len(meta_description) > 160:
            raise ValidationError('La description SEO ne peut pas dépasser 160 caractères.')
        return meta_description


class CommentaireForm(forms.ModelForm):
    """
    Formulaire pour les commentaires
    """
    class Meta:
        model = Commentaire
        fields = ['nom', 'email', 'site_web', 'contenu']
        
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre nom'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre email'
            }),
            'site_web': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre site web (optionnel)'
            }),
            'contenu': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Votre commentaire...'
            }),
        }
    
    def clean_contenu(self):
        contenu = self.cleaned_data.get('contenu')
        if len(contenu) < 10:
            raise ValidationError('Le commentaire doit contenir au moins 10 caractères.')
        if len(contenu) > 1000:
            raise ValidationError('Le commentaire ne peut pas dépasser 1000 caractères.')
        return contenu
    
    def clean_nom(self):
        nom = self.cleaned_data.get('nom')
        if nom and len(nom) < 2:
            raise ValidationError('Le nom doit contenir au moins 2 caractères.')
        return nom


class CategorieForm(forms.ModelForm):
    """
    Formulaire pour la création et modification de catégories
    """
    class Meta:
        model = Categorie
        fields = ['nom', 'description', 'couleur', 'icone', 'meta_description', 'actif']
        
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la catégorie'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description de la catégorie'
            }),
            'couleur': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color'
            }),
            'icone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fa-solid fa-brain (exemple)'
            }),
            'meta_description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Description SEO (160 caractères max)'
            }),
        }
    
    def clean_nom(self):
        nom = self.cleaned_data.get('nom')
        if len(nom) < 3:
            raise ValidationError('Le nom de la catégorie doit contenir au moins 3 caractères.')
        return nom


class TagForm(forms.ModelForm):
    """
    Formulaire pour la création de tags
    """
    class Meta:
        model = Tag
        fields = ['nom']
        
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du tag'
            }),
        }
    
    def clean_nom(self):
        nom = self.cleaned_data.get('nom')
        if len(nom) < 2:
            raise ValidationError('Le nom du tag doit contenir au moins 2 caractères.')
        return nom.lower()


class NewsletterForm(forms.ModelForm):
    """
    Formulaire d'abonnement à la newsletter
    """
    class Meta:
        model = AbonnementNewsletter
        fields = ['email', 'nom']
        
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre adresse email',
                'required': True
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre nom (optionnel)'
            }),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        
        # Vérifier si l'email n'est pas déjà abonné
        if AbonnementNewsletter.objects.filter(email=email, actif=True).exists():
            raise ValidationError('Cette adresse email est déjà abonnée à notre newsletter.')
        
        return email


class RechercheArticleForm(forms.Form):
    """
    Formulaire de recherche d'articles
    """
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rechercher des articles...'
        })
    )
    
    categorie = forms.ModelChoiceField(
        queryset=Categorie.objects.filter(actif=True),
        required=False,
        empty_label="Toutes les catégories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    tag = forms.ModelChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        empty_label="Tous les tags",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    SORT_CHOICES = [
        ('-date_publication', 'Plus récent'),
        ('date_publication', 'Plus ancien'),
        ('-vues', 'Plus vu'),
        ('-likes', 'Plus aimé'),
        ('titre', 'Titre A-Z'),
        ('-titre', 'Titre Z-A'),
    ]
    
    sort = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        initial='-date_publication',
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class ContactForm(forms.Form):
    """
    Formulaire de contact depuis le blog
    """
    nom = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre nom'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre email'
        })
    )
    
    sujet = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sujet de votre message'
        })
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Votre message...'
        })
    )
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 20:
            raise ValidationError('Le message doit contenir au moins 20 caractères.')
        return message


class ModerationCommentaireForm(forms.Form):
    """
    Formulaire pour la modération des commentaires
    """
    ACTION_CHOICES = [
        ('approuver', 'Approuver'),
        ('rejeter', 'Rejeter'),
        ('supprimer', 'Supprimer'),
        ('signaler', 'Signaler comme spam'),
    ]
    
    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    commentaire_ids = forms.CharField(widget=forms.HiddenInput())
    
    motif = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Motif de la modération (optionnel)'
        })
    )


    from .models import SoftSkill  # ⚠️ à vérifier si déjà importé

class SoftSkillForm(forms.ModelForm):
    """
    Formulaire pour créer et modifier des Soft Skills
    """
    class Meta:
        model = SoftSkill
        fields = ['nom', 'description']
        
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du Soft Skill'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description du Soft Skill'
            }),
        }
