import json, os, urllib, httplib, urllib2

from django import http
from django.shortcuts import render_to_response, redirect
from google.appengine.api import oauth
from oauth2client import client
from oauth2client.django_orm import Storage
from apiclient.discovery import build
from mainsite.models import CredentialsModel

class Youtube_API:
	scope = 'https://www.googleapis.com/auth/youtube'
	base_url = 'https://www.googleapis.com/youtube/v3'
	subscriptions_url = '%s/subscriptions/part=snippet&mine=true' % base_url
	channel_url = '%s/channels/?part=snippet&mine=true' % base_url

class UserInfo_API:
	scope = 'https://www.googleapis.com/auth/userinfo.email'
	query_url = 'https://www.googleapis.com/oauth2/v2/userinfo'

class AuthConfig:
	scopes = [Youtube_API.scope, UserInfo_API.scope]
	auth_url_base = 'https://accounts.google.com/o/oauth2/auth'
	exchange_request_url = 'accounts.google.com/o/oauth2/token'
	client_secret_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'client_secret.json')


def oauth2callback(request):
	## Read client secret file	
	with open(AuthConfig.client_secret_file, 'rb') as read_client_secret_file:
		client_secret = json.load(read_client_secret_file)

	flow = client.flow_from_clientsecrets(
		AuthConfig.client_secret_file,
		scope=AuthConfig.scopes,
		redirect_uri=client_secret['web']['redirect_uri'][0]
		)

	if request.GET.get('code') == '':
		auth_uri = flow.step1_get_authorize_url()
		return redirect(auth_uri)
	else:
		code = request.GET.get('code')
		credentials = flow.step2_exchange(auth_code)
		storage = Storage(CredentialsModel, 'id', 'TestingUser', 'credential')
		storage.put(credential)
		return redirect(r'/home')

def home(request):
	passed_dict = {}

	storage = Storage(CredentialsModel, 'id', 'TestingUser', 'credential')
	credential = storage.get()

	passed_dict['user_email'] = oauth.get_current_user(Youtube_API.scope)
	return render_to_response('home.html', passed_dic)


def login(request):
	passed_dict = {}
	return render_to_response('login.html', passed_dict) 

