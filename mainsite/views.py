import json, os
from django import http
from django.shortcuts import render_to_response

def home(request):
	passed_dict = {}
	return render_to_response('home.html', passed_dict)

def login_page(request):
	passed_dict = {}
	## Read client secret file
	client_secret_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'client_secret.json')
	with open(client_secret_file, 'rb') as read_client_secret_file:
		client_secret = json.load(read_client_secret_file)

	## Construct login URL
	scope = r'https://www.googleapis.com/auth/youtube'
	login_url_base = r'https://accounts.google.com/o/oauth2/auth'
	client_id = client_secret['web']['client_id']
	redirect_uri = client_secret['web']['redirect_uris'][0]
	login_url = '%s?client_id=%s&redirect_uri=%s&scope=%s&response_type=code&' % (
		login_url_base, client_id, redirect_uri, scope)

	passed_dict['login_url'] = login_url
	return render_to_response('login.html', passed_dict)
