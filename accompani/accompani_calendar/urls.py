from django.conf.urls import url

from . import views

# TODO(Ankit): Add mappings for oauth callback url
urlpatterns = [
    url(r'^oauthcallback/', views.auth_return, name='oauthcallback'),
    url(r'^list/', views.fetch_list, name='list_events'),
    # Catch all url
    url(r'^', views.index, name='index'),
]
