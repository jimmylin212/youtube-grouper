from django import http
from django.shortcuts import render_to_response, redirect
from google.appengine.api import oauth

from mainsite.py_modules.youtube_related import Youtube
from mainsite.py_modules.user_related import UserRelated

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
	youtube = Youtube()
	user_related = UserRelated()
	
	email = request.session.get('email')
	google_id = request.session.get('id')

	query_user_info = user_related.get_user_info(email=email)
	all_subscriptions = youtube.get_subscriptions(query_user_info)

	passed_dict['email'] = email
	passed_dict['all_subscriptions'] = all_subscriptions

	return render_to_response('my_subscriptions.html', passed_dict)


def login(request):
	passed_dict = {}
	return render_to_response('login.html', passed_dict) 

