from django import http
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from google.appengine.api import oauth

from mainsite.py_modules.youtube_related import Youtube
from mainsite.py_modules.user_related import UserRelated
from mainsite.py_modules.subscription_related import Subscription
from mainsite.py_modules.group_related import Group
from mainsite.py_modules.playlist_related import PlayList

def login(request):
	passed_dict = {}
	return render_to_response('login.html', passed_dict) 

def authentication(request):
	user_related = UserRelated()

	if request.GET.get('code') == None:
		auth_url = user_related.get_auth_url()
		return redirect(auth_url)
	else:
		email = user_related.authentication(code=request.GET.get('code'))
		request.session['email'] = email

		return redirect('/home')

def my_subscriptions(request):
	passed_dict = {}
	passed_dict.update(csrf(request))

	youtube = Youtube()
	user_related = UserRelated()
	subscription_related = Subscription()
	
	email = request.session.get('email')

	if request.method == "POST" and request.POST.get('form_action') == 'AddGroups':
		select_subscriptions = request.POST.getlist('select_subscriptions')
		group_name = request.POST.get('group_name')
		subscription_related.add_group(email, select_subscriptions, group_name)

	all_channels = youtube.get_subscriptions(email)

	## Check the subscription status every time use back to the page.
	subscription_related.upsert_channel(email, all_channels)

	channel_groups = subscription_related.get_channel_groups(email)
 
	passed_dict['email'] = email
	passed_dict['channel_groups'] = channel_groups

	return render_to_response('my_subscriptions.html', passed_dict)

def my_group(request, group_name):
	passed_dict = {}
	passed_dict.update(csrf(request))
	group = Group()
	playlist = PlayList()

	email = request.session.get('email')

	if request.method == "POST" and request.POST.get('form_action') == 'AddPlayList':
		select_videos = request.POST.getlist('select_videos')
		playlist.add_videos(email, select_videos)

	group_upload_videos = group.get_upload_viedos(email, group_name)

	passed_dict['group_upload_videos'] = group_upload_videos
	return render_to_response('my_group.html', passed_dict)

