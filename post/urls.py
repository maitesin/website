from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name="Post index"),
    url(r'^projects$', views.projects, name="List of projects"),
    url(r'^resume$', views.resume, name="My resume"),
    url(r'^about$', views.about, name="About this website"),
]
