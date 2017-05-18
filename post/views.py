from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

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
        return self.model.get_posts_from_year_month_day_title(self.kwargs['year'], self.kwargs['month'], self.kwargs['day'], self.kwargs['title'])

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['absolute_uri'] = self.request.build_absolute_uri()
        return context

class LatestPostFeed(Feed):
    title = "Oscar Forner's personal website"
    link = '/rss/'
    description = "I am a software engineer at VCA Technology. Passionate about GNU/Linux and Open Source. Interested in system programming languages, operating systems and compilers."

    def items(self):
        return Post.get_latest_posts(10)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.get_abstract()

    def item_link(self, item):
        print("Getting URL: %s" % item.get_url())
        return item.get_url()

class LatestPostAtom(LatestPostFeed):
    feed_type = Atom1Feed
    subtitle = LatestPostFeed.description

def projects(request):
    context = {'projects' : [{'title':'Trie, TST & Radix Tree', 'url':'tries', 'img':'tries.png'},
                             {'title':'ACC (ARM C Compiler)', 'url':'acc', 'img':'acc.png'},
                             {'title':'Personal website', 'url':'website', 'img':'website.png'},
                             {'title':'Placeholder 4', 'url':'place4', 'img':'place4.png'},
                             {'title':'Placeholder 5', 'url':'place5', 'img':'place5.png'},
                             {'title':'Placeholder 6', 'url':'place6', 'img':'place6.png'}]}
    return render(request, 'projects.html', context)

def tries(request):
    return render(request, 'tries.html', {})

def acc(request):
    return render(request, 'acc.html', {})

def personal(request):
    return render(request, 'personal.html', {})

def resume(request):
    context = {}
    return render(request, 'resume.html', context)

def about(request):
    context = {}
    return render(request, 'about.html', context)
