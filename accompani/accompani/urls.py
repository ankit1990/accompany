from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'^accompani/calendar/', include('accompani_calendar.urls')),
                       )
