from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^home/$', 'mainsite.views.home'),
    url(r'^login/$', 'mainsite.views.login_page'),
)
