from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView

from .models import Tag, Post, Category, PostTag

class PostListView(ListView):
    model = Post

    def get_template_names(self):
        return ['blog.html']

    def get_queryset(self):
        return self.model.get_latest_posts(5)

def year(request, year):
    context = {}
    return render(request, 'year.html', context)

def month(request, year, month):
    context = {}
    return render(request, 'month.html', context)

def day(request, year, month, day):
    context = {}
    return render(request, 'day.html', context)

def post(request, year, month, day, title):
    context = {}
    return render(request, 'post.html', context)

def category(request, name):
    context = {}
    return render(request, 'category.html', context)

def tag(request, name):
    context = {}
    return render(request, 'tag.html', context)

def projects(request):
    context = {}
    return render(request, 'projects.html', context)

def resume(request):
    context = {}
    return render(request, 'resume.html', context)

def about(request):
    context = {}
    return render(request, 'about.html', context)
