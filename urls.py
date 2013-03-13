from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dicziunari-web.views.home', name='home'),
    # url(r'^dicziunari/', include('dicziunari-web.foo.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^accounts/', include('registration.urls')),
    url(r'^selectable/', include('selectable.urls')),

    url(r'^tschercha/', include('tschercha.urls')),
    url(r'^$', 'tschercha.views.tschercha', name='tschercha'),
)
