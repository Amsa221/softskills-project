from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Bienvenue sur le site Soft Skills</h1>")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home),  # 👈 page d'accueil
    path('skills/', include('skills.urls')),
]



