from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name="Index"),
    url(r'^(?P<year>[0-9]{4})$', views.year, name="Year"),
    url(r'^(?P<year>[0-9]{4})/$', views.year, name="YearSlash"),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})$', views.month, name="Month"),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month, name="MonthSlash"),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]+)$', views.day, name="Day"),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]+)/$', views.day, name="DaySlash"),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]+)/(?P<title>\w+)$', views.post, name="Post"),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]+)/(?P<title>\w+)/$', views.post, name="PostSlash"),
    url(r'^tag/(?P<name>\w+)$', views.tag, name="Tag"),
    url(r'^tag/(?P<name>\w+)/$', views.tag, name="TagSlash"),
    url(r'^category/(?P<name>\w+)$', views.category, name="Category"),
    url(r'^category/(?P<name>\w+)/$', views.category, name="CategorySlash"),
    url(r'^projects$', views.projects, name="Projects"),
    url(r'^resume$', views.resume, name="Resume"),
    url(r'^about$', views.about, name="About"),
]
