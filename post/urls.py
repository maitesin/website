from django.conf.urls import url, handler404

from . import views

urlpatterns = [
    url(r'^$', views.IndexPostListView.as_view(), name="Blog"),
    url(r'^(?P<year>[0-9]{4})/?$', views.YearPostListView.as_view(), name="Year"),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/?$', views.MonthPostListView.as_view(), name="Month"),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]+)/?$', views.DayPostListView.as_view(), name="Day"),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]+)/(?P<title>\w+)/?$', views.PostDetailView.as_view(), name="Post"),
    url(r'^tag/(?P<name>\w+)/?$', views.TagPostListView.as_view(), name="Tag"),
    url(r'^category/(?P<name>\w+)/?$', views.CategoryPostListView.as_view(), name="Category"),
    url(r'^all/?$', views.AllPostListView.as_view(), name="All"),
    url(r'^projects/?$', views.projects, name="Projects"),
    url(r'^projects/tries?$', views.tries, name="Tries"),
    url(r'^projects/acc?$', views.acc, name="ACC"),
    url(r'^projects/website?$', views.website, name="Website"),
    url(r'^resume/?$', views.resume, name="Resume"),
    url(r'^about/?$', views.about, name="About"),
    url(r'^rss/?$', views.LatestPostFeed(), name="RSS"),
    url(r'^atom/$', views.LatestPostAtom(), name="Atom"),
]

handler404 = 'post.views.handler404'
handler500 = 'post.views.handler500'
