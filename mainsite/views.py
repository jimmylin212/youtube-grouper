import json, os, urllib, httplib, urllib2

from django import http
from django.shortcuts import render_to_response, redirect
from google.appengine.api import oauth


class Youtube_API:
	base_url = 'https://www.googleapis.com/youtube/v3'
	subscriptions_url = '%s/subscriptions/part=snippet&mine=true' % base_url
	channel_url = '%s/channels/?part=snippet&mine=true' % base_url

class UserInfo_API:
	query_url = 'https://www.googleapis.com/oauth2/v2/userinfo'

class AuthConfig:
	scopes = ['https://www.googleapis.com/auth/youtube',
			  'https://www.googleapis.com/auth/userinfo.email']
	
	auth_url_base = 'https://accounts.google.com/o/oauth2/auth'
	get_token_url = 'accounts.google.com/o/oauth2/token'
	client_secret_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'client_secret.json')

def authentication(request):
	## Read client secret file	
	with open(AuthConfig.client_secret_file, 'rb') as read_client_secret_file:
		client_secret = json.load(read_client_secret_file)

	if request.GET.get('code') == None:
		auth_url = '%s?scope=%s&client_id=%s&redirect_uri=%s&response_type=code' % (
			AuthConfig.auth_url_base, ' '.join(AuthConfig.scopes),
			client_secret['web']['client_id'], client_secret['web']['redirect_uris'][0])

		return redirect(auth_url)
	else:
		code = request.GET.get('code')
		parameters = urllib.urlencode({'code' : code, 'grant_type' : 'authorization_code',
			'client_id' : client_secret['web']['client_id'], 
			'client_secret' : client_secret['web']['client_secret'],
			'redirect_uri' : client_secret['web']['redirect_uris'][0]})

		connection = httplib.HTTPSConnection(AuthConfig.get_token_url)
		connection.request("POST", "", parameters)
		response = connection.getresponse()
		status = response.status
		tokens = json.loads(response.read())
		
		## Query user info to get the user's emaiil address and id
		user_info_request = urllib2.Request(url=UserInfo_API.query_url)
		user_info_request.add_header('Authorization', 'Bearer %s' % tokens['access_token'])
		user_info_response = urllib2.urlopen(user_info_request)
		user_info_response = json.loads(user_info_response.read())

		return redirect('/home')

def home(request):
	passed_dict = {}

	# storage = Storage(CredentialsModel, 'id', 'TestingUser', 'credential')
	# credential = storage.get()

	# passed_dict['user_email'] = oauth.get_current_user(Youtube_API.scope)
	return render_to_response('home.html', passed_dict)


def login(request):
	passed_dict = {}
	return render_to_response('login.html', passed_dict) 

