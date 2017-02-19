from django.shortcuts import render
from django.http import HttpResponse

from .models import Tag, Post, Category, PostTag

def index(request):
    context = {}
    return render(request, 'blog.html', context)

def projects(request):
    context = {}
    return render(request, 'projects.html', context)

def resume(request):
    context = {}
    return render(request, 'resume.html', context)

def about(request):
    context = {}
    return render(request, 'about.html', context)
