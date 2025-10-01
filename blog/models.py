from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Categorie(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['nom']

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.nom)[:110]
            slug = base
            counter = 1
            while Categorie.objects.filter(slug=slug).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Article(models.Model):
    STATUT_CHOICES = (
        ('draft', 'Brouillon'),
        ('published', 'Publié'),
    )

    titre = models.CharField(max_length=250)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    contenu = models.TextField()
    image = models.ImageField(upload_to='articles/', null=True, blank=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, related_name='articles')
    auteur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='articles')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='draft')
    meta_description = models.CharField(max_length=300, blank=True)
    mots_cles = models.CharField(max_length=300, blank=True, help_text="Sépare les mots-clés par des virgules")

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['-date_creation']

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        # génération slug si absent
        if not self.slug:
            base = slugify(self.titre)[:280]
            slug = base
            counter = 1
            while Article.objects.filter(slug=slug).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def extrait(self):
        return (self.contenu[:300] + '...') if len(self.contenu) > 300 else self.contenu


class Commentaire(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='commentaires')
    auteur = models.CharField(max_length=150)
    auteur_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='commentaires')
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    valide = models.BooleanField(default=False)  # modération manuelle par défaut
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='reponses')

    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
        ordering = ['-date_creation']

    def __str__(self):
        return f"Commentaire de {self.auteur} sur {self.article.titre[:30]}"
