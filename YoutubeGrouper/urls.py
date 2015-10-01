from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^login/$', 'mainsite.views.login'),
    url(r'^my_subscriptions/$', 'mainsite.views.my_subscriptions'),
    url(r'^authentication/$', 'mainsite.views.authentication'),
)
