from django.conf.urls import url

from . import views

# TODO(Ankit): Add mappings for oauth callback url
urlpatterns = [
    url(r'^oauthcallback/', views.auth_return, name='oauthcallback'),
    url(r'^index/', views.index, name='index'),
]
