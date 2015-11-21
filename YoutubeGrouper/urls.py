from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^login/$', 'mainsite.views.login'),
    url(r'^my_subscriptions/$', 'mainsite.views.my_subscriptions'),
    url(r'^my_group/(\w+)$', 'mainsite.views.my_group'),
    url(r'^my_playlist/$', 'mainsite.views.my_playlist'),
    url(r'^watch_video/([\w\d\-]+)/$', 'mainsite.views.watch_video'),
    url(r'^authentication/$', 'mainsite.views.authentication'),
    ## Cronjob start
    url(r'^get_daily_uploaded_video/$', 'mainsite.views.get_daily_uploaded_video'),
    url(r'^daily_check_video_status/$', 'mainsite.views.daily_check_video_status'),
    url(r'^daily_check_channel_status/$', 'mainsite.views.daily_check_channel_status'),
    url(r'^perge_old_videos/$', 'mainsite.views.perge_old_videos'),
    ## Cronjob end
    url(r'^$', 'mainsite.views.home'),
)
