from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Tag, Post, Category, PostTag

class PostListView(ListView):
    model = Post

    def get_template_names(self):
        return ['blog.html']

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['title'] = self.get_page_title()
        return context

class IndexPostListView(PostListView):
    def get_page_title(self):
        return 'Latest posts'

    def get_queryset(self):
        return self.model.get_latest_posts(5)

class YearPostListView(PostListView):
    def get_page_title(self):
        return 'Posts from %s' % self.kwargs['year']

    def get_queryset(self):
        return self.model.get_posts_from_year(self.kwargs['year'])

class MonthPostListView(PostListView):
    def get_page_title(self):
        return 'Posts from %s %s' % (self.kwargs['month'], self.kwargs['year'])

    def get_queryset(self):
        return self.model.get_posts_from_year_month(self.kwargs['year'], self.kwargs['month'])

class DayPostListView(PostListView):
    def get_page_title(self):
        return 'Posts from %s %s %s' % (self.kwargs['day'], self.kwargs['month'], self.kwargs['year'])

    def get_queryset(self):
        return self.model.get_posts_from_year_month_day(self.kwargs['year'], self.kwargs['month'], self.kwargs['day'])

class CategoryPostListView(PostListView):
    def get_page_title(self):
        return 'Category %s' % Category.get_category_with_title(self.kwargs['name'])

    def get_queryset(self):
        return self.model.get_latest_posts_with_category(self.kwargs['name'])

class TagPostListView(PostListView):
    def get_page_title(self):
        return 'Tag %s' % Tag.get_tag_with_title(self.kwargs['name'])

    def get_queryset(self):
        return self.model.get_latest_posts_with_tag(self.kwargs['name'])

class AllPostListView(PostListView):
    def get_page_title(self):
        return 'All posts'

    def get_queryset(self):
        return self.model.get_latest_posts()

class PostDetailView(DetailView):
    model = Post

    def get_template_names(self):
        return ['post.html']

    def get_object(self):
        for post in self.model.get_posts_from_year_month_day(self.kwargs['year'], self.kwargs['month'], self.kwargs['day']):
            if post.get_title() == self.kwargs['title']:
                return post
        raise Http404("Post does not exist")

def projects(request):
    context = {}
    return render(request, 'projects.html', context)

def resume(request):
    context = {}
    return render(request, 'resume.html', context)

def about(request):
    context = {}
    return render(request, 'about.html', context)
