import json, os, urllib, httplib, urllib2
from django import http
from django.shortcuts import render_to_response

class AuthConfig:
	scope = r'https://www.googleapis.com/auth/youtube'
	auth_url_base = r'https://accounts.google.com/o/oauth2/auth'
	exchange_request_url = r'accounts.google.com/o/oauth2/token'
	client_secret_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'client_secret.json')

class Youtube_API:
	base_url = r'https://www.googleapis.com/youtube/v3'
	subscriptions_url = '%s/subscriptions/part=snippet&mine=true' % base_url
	channel_url = '%s/channels/?part=snippet&mine=true' % base_url


def welcome(request):
	passed_dict = {}
	return render_to_response('home.html', passed_dict) 

def home(request):
	passed_dict = {}
	return render_to_response('home.html', passed_dict)

def login_page(request):
	passed_dict = {}

	## Read client secret file	
	with open(AuthConfig.client_secret_file, 'rb') as read_client_secret_file:
		client_secret = json.load(read_client_secret_file)

	## Construct login URL	
	client_id = client_secret['web']['client_id']
	redirect_uri = client_secret['web']['redirect_uris'][0]
	login_url = '%s?client_id=%s&redirect_uri=%s&scope=%s&response_type=code&' % (
		AuthConfig.auth_url_base, client_id, redirect_uri, AuthConfig.scope)

	passed_dict['login_url'] = login_url
	return render_to_response('login.html', passed_dict)

def exchange_auth(request):
	## Read client secret file
	with open(AuthConfig.client_secret_file, 'rb') as read_client_secret_file:
		client_secret = json.load(read_client_secret_file)

	code = request.GET.get('code')
	params = {'code' : code, 
			  'client_id' : client_secret['web']['client_id'],
			  'client_secret' : client_secret['web']['client_secret'], 
			  'redirect_uri' : client_secret['web']['redirect_uris'][0],
			  'grant_type' : 'authorization_code'
			  }

	auth_api_connection = httplib.HTTPSConnection(AuthConfig.exchange_request_url)
	auth_api_connection.request('POST', '', urllib.urlencode(params))
	auth_api_response = auth_api_connection.getresponse()

	if auth_api_response.status == 200:
		auth_api_response = json.loads(auth_api_response.read())
		user_channel_query_url = '%s&access_token=%s' % (Youtube_API.channel_url, auth_api_response['access_token'])

		user_channel_response = urllib.urlopen(user_channel_query_url)
		user_channel_response = json.loads(user_channel_response.read())
		
	return render_to_response('home.html')
