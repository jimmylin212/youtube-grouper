from django import http
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from google.appengine.api import oauth

from mainsite.py_modules.youtube_related import Youtube
from mainsite.py_modules.user_related import UserRelated
from mainsite.py_modules.subscription_related import Subscription
from mainsite.py_modules.group_related import Group
from mainsite.py_modules.playlist_related import PlayList
from mainsite.py_modules.cronjob import CronJob

def login(request):
	passed_dict = {}
	return render_to_response('login.html', passed_dict)

def home(request):
	return redirect('/my_subscriptions')

def authentication(request):
	user_related = UserRelated()

	if request.GET.get('code') == None:
		auth_url = user_related.get_auth_url()
		return redirect(auth_url)
	else:
		email = user_related.authentication(code=request.GET.get('code'))
		request.session['email'] = email

		return redirect('/my_subscriptions')

def my_subscriptions(request):
	passed_dict = {}
	passed_dict.update(csrf(request))

	youtube = Youtube()
	user_related = UserRelated()
	subscription_related = Subscription()

	email = request.session.get('email')
	if email == None:
		return redirect('/login')

	if request.method == "POST" and request.POST.get('form_action') == 'AddGroups':
		select_subscriptions = request.POST.getlist('select_subscriptions')
		group_names = request.POST.get('tags')
		subscription_related.add_group(email, select_subscriptions, group_names)
	elif request.method == "POST" and request.POST.get('form_action') == 'Update':
		all_channels = youtube.get_subscriptions(email)
		new_channel_count, removed_channel_count = subscription_related.upsert_channel(email, all_channels)
		passed_dict['new_channel_count'] = new_channel_count
		passed_dict['removed_channel_count'] = removed_channel_count

	channel_groups, no_groups = subscription_related.get_channel_groups(email)

	passed_dict['email'] = email
	passed_dict['channel_groups'] = channel_groups
	passed_dict['no_groups'] = no_groups

	return render_to_response('my_subscriptions.html', passed_dict)

def my_group(request, group_name):
	passed_dict = {}
	passed_dict.update(csrf(request))
	group = Group()
	playlist = PlayList()

	email = request.session.get('email')
	if email == None:
		return redirect('/login')

	if request.method == "POST" and request.POST.get('form_action') == 'AddPlayList':
		select_videos = request.POST.getlist('select_videos')
		playlist.add_videos(email, select_videos)
		return redirect('/my_playlist/')
	elif request.method == "POST" and request.POST.get('form_action') == 'RemoveTag':
		group.remove_group(email, group_name)
		return redirect('/my_subscriptions/')

	upload_videos = group.get_upload_viedos(email, group_name)

	passed_dict['group_upload_videos'] = upload_videos
	passed_dict['group_name'] = group_name
	return render_to_response('my_group.html', passed_dict)

def my_playlist(request):
	passed_dict = {}
	passed_dict.update(csrf(request))
	youtube = Youtube()
	playlist = PlayList()

	email = request.session.get('email')
	if email == None:
		return redirect('/login')

	playlist_id = playlist.check_playlist_exisxtence(email)

	if request.method == 'POST' and request.POST.get('form_action') == 'RemoveWatched':
		watchhistory_playlist_id = playlist.get_watch_history_playlist_id(email)
		youtube.remove_watched_from_playlist(email, playlist_id, watchhistory_playlist_id)
	elif request.method == 'POST' and request.POST.get('form_action') == 'RemoveAll':
		youtube.remove_all_from_playlist(email, playlist_id)

	playlist_id = playlist.check_playlist_exisxtence(email)

	passed_dict['playlist_id'] = playlist_id
	return render_to_response('my_playlist.html', passed_dict)

def watch_video(request, video_id):
	passed_dict = {}
	passed_dict.update(csrf(request))

	passed_dict['video_id'] = video_id
	return render_to_response('watch_video.html', passed_dict)

def get_daily_uploaded_video(request):
	cronjob = CronJob()
	cronjob.get_daily_uplaod_videos()

	return render_to_response('dummy_cronjob_page.html')

def daily_check_video_status(request):
	cronjob = CronJob()
	cronjob.daily_check_video_status()
	return render_to_response('dummy_cronjob_page.html')

def daily_check_channel_status(request):
	cronjob = CronJob()
	cronjob.daily_check_channel_status()
	return render_to_response('dummy_cronjob_page.html')

def perge_old_videos(request):
	cronjob = CronJob()
	cronjob.perge_old_videos()
	return render_to_response('dummy_cronjob_page.html')
