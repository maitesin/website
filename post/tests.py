from django.test import TestCase
from django.utils import timezone

from django.contrib.auth.models import User
from .models import Post, Category, Tag, PostTag


class PostTests(TestCase):

    def setUp(self):
        my_user = User()
        my_user.save()

        category_1 = Category(name="Category 1")
        category_1.save()
        category_2 = Category(name="Category 2")
        category_2.save()

        tag_1 = Tag(name="Tag 1")
        tag_1.save()
        tag_2 = Tag(name="Tag 2")
        tag_2.save()
        tag_3 = Tag(name="Tag 3")
        tag_3.save()
        tag_4 = Tag(name="Tag 4") # Not used
        tag_4.save()

        now = timezone.now()
        post_1 = Post(author=my_user, title="Post 1", content="Content of the first post", category=category_1, pub_date=now)
        post_1.save()
        post_2 = Post(author=my_user, title="Post 2", content="Content of the second post", category=category_2, pub_date=now + timezone.timedelta(days=1))
        post_2.save()
        post_3 = Post(author=my_user, title="Post 4", content="Content of the forth post", category=category_2, pub_date=now + timezone.timedelta(days=3))
        post_3.save()
        post_4 = Post(author=my_user, title="Post 5", content="Content of the fifth post", category=category_1, pub_date=now + timezone.timedelta(days=4))
        post_4.save()
        post_5 = Post(author=my_user, title="Post 3", content="Content of the third post", category=category_1, pub_date=now + timezone.timedelta(days=2))
        post_5.save()
        post_6 = Post(author=my_user, title="Post 7", content="Content of the seventh post", category=category_1, pub_date=now + timezone.timedelta(days=6))
        post_6.save()
        post_7 = Post(author=my_user, title="Post 8", content="Content of the eighth post", category=category_2, pub_date=now + timezone.timedelta(days=7))
        post_7.save()
        post_8 = Post(author=my_user, title="Post 9", content="Content of the ninth post", category=category_1, pub_date=now + timezone.timedelta(days=8))
        post_8.save()
        post_9 = Post(author=my_user, title="Post 6", content="Content of the sixth post", category=category_2, pub_date=now + timezone.timedelta(days=5))
        post_9.save()
        post_10 = Post(author=my_user, title="Post 10", content="Content of the tenth post", category=category_2, pub_date=now + timezone.timedelta(days=9))
        post_10.save()
        post_11 = Post(author=my_user, title="Post 11", content="Content of the eleventh post", category=category_1, pub_date=now + timezone.timedelta(days=10))
        post_11.save()

        PostTag(post=post_1, tag=tag_1).save()
        PostTag(post=post_1, tag=tag_2).save()
        PostTag(post=post_2, tag=tag_1).save()
        PostTag(post=post_2, tag=tag_2).save()
        PostTag(post=post_3, tag=tag_3).save()
        PostTag(post=post_4, tag=tag_2).save()
        PostTag(post=post_5, tag=tag_1).save()
        PostTag(post=post_6, tag=tag_2).save()
        PostTag(post=post_6, tag=tag_3).save()
        PostTag(post=post_6, tag=tag_1).save()
        PostTag(post=post_7, tag=tag_2).save()
        PostTag(post=post_7, tag=tag_3).save()
        PostTag(post=post_8, tag=tag_2).save()
        PostTag(post=post_9, tag=tag_3).save()
        PostTag(post=post_10, tag=tag_3).save()
        PostTag(post=post_11, tag=tag_3).save()

    def tearDown(self):
        Post.objects.all().delete()
        Category.objects.all().delete()
        Tag.objects.all().delete()
        PostTag.objects.all().delete()

    def test_get_all_posts(self):
        latest = Post.get_latest_posts()
        self.assertEquals(len(latest), 11)

    def test_latest_posts_are_working_when_no_post(self):
        self.tearDown() # To remove the content of the database
        latest = Post.get_latest_posts(5)
        self.assertEquals(list(latest), [])

    def test_latest_posts_with_10_when_5_are_avaiable(self):
        latest_10 = Post.get_latest_posts(10)
        self.assertEquals(len(latest_10), 10)
        self.assertEquals(latest_10[0].title, "Post 11")
        self.assertEquals(latest_10[1].title, "Post 10")
        self.assertEquals(latest_10[2].title, "Post 9")
        self.assertEquals(latest_10[3].title, "Post 8")
        self.assertEquals(latest_10[4].title, "Post 7")
        self.assertEquals(latest_10[5].title, "Post 6")
        self.assertEquals(latest_10[6].title, "Post 5")
        self.assertEquals(latest_10[7].title, "Post 4")
        self.assertEquals(latest_10[8].title, "Post 3")
        self.assertEquals(latest_10[9].title, "Post 2")

    def test_latest_posts_with_category(self):
        latest_with_category_1 = Post.get_latest_posts_with_category("Category 1")
        self.assertEquals(len(latest_with_category_1), 6)
        self.assertEquals(latest_with_category_1[0].title, "Post 11")
        self.assertEquals(latest_with_category_1[1].title, "Post 9")
        self.assertEquals(latest_with_category_1[2].title, "Post 7")
        self.assertEquals(latest_with_category_1[3].title, "Post 5")
        self.assertEquals(latest_with_category_1[4].title, "Post 3")
        self.assertEquals(latest_with_category_1[5].title, "Post 1")

    def test_latest_posts_with_invalid_category(self):
        latest_with_category_invalid = Post.get_latest_posts_with_category("Category Invalid")
        self.assertEquals(latest_with_category_invalid, None)

    def test_latest_posts_with_tag(self):
        latest_with_tag_1 = Post.get_latest_posts_with_tag("Tag 1")
        self.assertEquals(len(latest_with_tag_1), 4)
        self.assertEquals(latest_with_tag_1[0].title, "Post 1")
        self.assertEquals(latest_with_tag_1[1].title, "Post 2")
        self.assertEquals(latest_with_tag_1[2].title, "Post 3")
        self.assertEquals(latest_with_tag_1[3].title, "Post 7")

    def test_posts_with_empty_tag(self):
        latest_with_tag_4 = Post.get_latest_posts_with_tag("Tag 4")
        self.assertEquals(latest_with_tag_4, [])

    def test_posts_with_invalid_tag(self):
        latest_with_tag_invalid = Post.get_latest_posts_with_tag("Tag Invalid")
        self.assertEquals(latest_with_tag_invalid, None)

    def test_post_get_title(self):
        now = timezone.now()
        title_from_post = Post(author=User(), title="Post 11", content="Content of the eleventh post", category=Category(name="Category"), pub_date=now).get_title()
        self.assertEquals(title_from_post, "Post_11")

    def test_post_get_url(self):
        now = timezone.now()
        url_from_post = Post(author=User(), title="Post 11", content="Content of the eleventh post", category=Category(name="Category"), pub_date=now).get_url()
        self.assertEquals(url_from_post, "/%s/%02d/%02d/Post_11" % (now.year, now.month, now.day))

    def test_category_get_title(self):
        title_from_category = Category(name="Category 1").get_title()
        self.assertEquals(title_from_category, "Category_1")

    def test_category_get_url(self):
        url_from_category = Category(name="Category 1").get_url()
        self.assertEquals(url_from_category, "/category/Category_1")

    def test_tag_get_title(self):
        title_from_tag = Tag(name="Tag 1").get_title()
        self.assertEquals(title_from_tag, "Tag_1")

    def test_tag_get_url(self):
        url_from_tag = Tag(name="Tag 1").get_url()
        self.assertEquals(url_from_tag, "/tag/Tag_1")
