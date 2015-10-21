from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^login/$', 'mainsite.views.login'),
    url(r'^my_subscriptions/$', 'mainsite.views.my_subscriptions'),
    url(r'^my_group/(\w+)$', 'mainsite.views.my_group'),
    url(r'^my_playlist/$', 'mainsite.views.my_playlist'),
    url(r'^authentication/$', 'mainsite.views.authentication'),
    url(r'^get_daily_uploaded_video/$', 'mainsite.views.get_daily_uploaded_video'),
)
