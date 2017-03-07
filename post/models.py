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
        posts = Post.objects.order_by('-pub_date')
        return posts if number is None else posts[:number]

    @staticmethod
    def get_latest_posts_with_category(category_name, number = None):
        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            return None
        posts = Post.get_latest_posts().filter(category=category)
        return posts if number is None else posts[:number]

    @staticmethod
    def get_latest_posts_with_tag(tag_name, number = None):
        try:
            tag = Tag.objects.get(name=tag_name)
        except Tag.DoesNotExist:
            return None
        post_tag = PostTag.objects.filter(tag=tag)
        return [elem.post for elem in post_tag]

    def get_title(self):
        return ''.join([char if char.isalnum() else '_' for char in self.title])

    def get_url(self):
        time = self.pub_date
        return reverse('Post', args=["%04d" % time.year, "%02d" % time.month, "%02d" % time.day, self.get_title()])

    # TODO: Create unit test for this method
    def get_content(self):
        return markdown(self.content, output_format="html5")

    # TODO: Create unit test for this method
    def get_abstract(self):
        cleanr = re.compile('<.*?>')
        return re.sub(cleanr, '', self.get_content())[:200] + '...'

    # TODO: Create unit test for this method
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
