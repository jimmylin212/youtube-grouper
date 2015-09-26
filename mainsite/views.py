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
		email, google_id = user_related.authentication(code=request.GET.get('code'))
		request.session['email'] = email
		request.session['google_id'] = google_id

		return redirect('/home')

def home(request):
	passed_dict = {}
	youtube = Youtube()
	user_related = UserRelated()
	
	email = request.session.get('email')
	google_id = request.session.get('id')

	query_user_info = user_related.get_user_info(email=email, google_id=google_id)
	youtube.get_subscriptions(query_user_info)
	b = c
	passed_dict['email'] = email
	passed_dict['google_id'] = google_id
	return render_to_response('home.html', passed_dict)


def login(request):
	passed_dict = {}
	return render_to_response('login.html', passed_dict) 

