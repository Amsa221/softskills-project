from django.shortcuts import render
from .models import Skill

def skills_list(request):
    skills = Skill.objects.all()
    return render(request, 'skills/skills_list.html', {'skills': skills})
