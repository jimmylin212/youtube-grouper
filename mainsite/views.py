from django import http
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from google.appengine.api import oauth

from mainsite.py_modules.youtube_related import Youtube
from mainsite.py_modules.user_related import UserRelated
from mainsite.py_modules.subscription_related import Subscription

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
		subscription_related.add_group_name(email, select_subscriptions, group_name)

	query_user_info = user_related.get_user_info(email=email)
	all_channels = youtube.get_subscriptions(query_user_info)

	## Check the subscription status every time use back to the page.
	all_channels = subscription_related.upsert_subscriptions(email, all_channels)
	grouped_channels = subscription_related.create_group_based_dict(all_channels)
 
	passed_dict['email'] = email
	passed_dict['grouped_channels'] = grouped_channels

	return render_to_response('my_subscriptions.html', passed_dict)

