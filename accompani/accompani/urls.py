from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^accompani/calendar/', include('accompani_calendar.urls')),
                       url(r'^accompani/admin/', include(admin.site.urls)),
                       )
