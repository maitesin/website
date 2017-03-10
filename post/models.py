from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from markdown import markdown
import re


class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    @staticmethod
    def get_list_of_tags():
        return Tag.objects.all()

    # TODO: Add test
    @staticmethod
    def get_tag_with_title(title):
        for tag in Tag.objects.all():
            if tag.get_title() == title:
                return tag
        return None

    def get_title(self):
        return ''.join([char if char.isalnum() else '_' for char in self.name])

    def get_url(self):
        return reverse('Tag', args=[self.get_title()])

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    @staticmethod
    def get_list_of_categories():
        return Category.objects.all()

    # TODO: Add test
    @staticmethod
    def get_category_with_title(title):
        for category in Category.objects.all():
            if category.get_title() == title:
                return category
        return None

    def get_title(self):
        return ''.join([char if char.isalnum() else '_' for char in self.name])

    def get_url(self):
        return reverse('Category', args=[self.get_title()])

class Post(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.ForeignKey(Category)
    pub_date = models.DateField()
    draft = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    @staticmethod
    def get_latest_posts(number = None):
        posts = Post.objects.order_by('-pub_date').filter(draft=False)
        return posts if number is None else posts[:number]

    @staticmethod
    def get_latest_posts_with_category(category_name, number = None):
        category = Category.get_category_with_title(category_name)
        posts = Post.get_latest_posts().filter(category=category)
        return posts if number is None else posts[:number]

    @staticmethod
    def get_latest_posts_with_tag(tag_name, number = None):
        tag = Tag.get_tag_with_title(tag_name)
        post_tag = PostTag.objects.filter(tag=tag)
        return [elem.post for elem in post_tag]

    # TODO: Add test
    @staticmethod
    def get_posts_from_year(year):
        return Post.objects.order_by('-pub_date').filter(draft=False).filter(pub_date__year=year)

    # TODO: Add test
    @staticmethod
    def get_posts_from_year_month(year, month):
        return Post.objects.order_by('-pub_date').filter(draft=False).filter(pub_date__year=year).filter(pub_date__month=month)

    # TODO: Add test
    @staticmethod
    def get_posts_from_year_month_day(year, month, day):
        return Post.objects.order_by('-pub_date').filter(draft=False).filter(pub_date__year=year).filter(pub_date__month=month).filter(pub_date__day=day)

    def get_title(self):
        return ''.join([char if char.isalnum() else '_' for char in self.title])

    def get_url(self):
        time = self.pub_date
        return reverse('Post', args=["%04d" % time.year, "%02d" % time.month, "%02d" % time.day, self.get_title()])

    def get_content(self):
        return markdown(self.content, output_format="html5")

    def get_abstract(self):
        cleanr = re.compile('<.*?>')
        return re.sub(cleanr, '', self.get_content())[:200] + '...'

    def get_tags(self):
        post_tag = PostTag.objects.filter(post=self)
        return [elem.tag for elem in post_tag]

class PostTag(models.Model):
    class Meta:
        unique_together = ('post', 'tag')
    post = models.ForeignKey(Post)
    tag = models.ForeignKey(Tag)

    def __str__(self):
        return "%d (Post: %s; Tag: %s)" % (self.id, self.post, self.tag)
