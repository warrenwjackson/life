from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/', 'track.views.loginview', name='login'),
    url(r'^auth/', 'track.views.sign_up_in', name='sign_up_in'),
    url(r'^day/', 'track.views.day', name='day'),
#    url(r'^static/(?P<path>.*)$', name='serve'),
    url(r'^summary/', 'track.views.summary', name='summary'),
    url(r'^$', 'track.views.entry', name='entry'),
 
    # Examples:
    # url(r'^$', 'life.views.home', name='home'),
    # url(r'^life/', include('life.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
