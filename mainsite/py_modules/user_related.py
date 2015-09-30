import json, os, urllib, httplib, urllib2, datetime
from db_utility import DBUtility

class UserRelated:
	scopes = ['https://www.googleapis.com/auth/youtube',
			  'https://www.googleapis.com/auth/userinfo.email']
	auth_token_url = 'accounts.google.com/o/oauth2/token'	
	auth_url_base = 'https://accounts.google.com/o/oauth2/auth'
	user_info_query_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
	client_secret_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'client_secret.json')

	def get_auth_url(self):
		## Read client secret file	
		with open(UserRelated.client_secret_file, 'rb') as read_client_secret_file:
			client_secret = json.load(read_client_secret_file)

		auth_url = '%s?scope=%s&client_id=%s&redirect_uri=%s&response_type=code&access_type=offline&approval_prompt=force' % (
			UserRelated.auth_url_base, ' '.join(UserRelated.scopes),
			client_secret['web']['client_id'], client_secret['web']['redirect_uris'][0])

		return auth_url

	def authentication(self, code):
		## Read client secret file	
		with open(UserRelated.client_secret_file, 'rb') as read_client_secret_file:
			client_secret = json.load(read_client_secret_file)

		parameters = urllib.urlencode({
			'code' : code, 
			'grant_type' : 'authorization_code',
			'client_id' : client_secret['web']['client_id'], 
			'client_secret' : client_secret['web']['client_secret'],
			'redirect_uri' : client_secret['web']['redirect_uris'][0]})

		connection = httplib.HTTPSConnection(UserRelated.auth_token_url)
		connection.request("POST", "", parameters)
		response = connection.getresponse()
		status = response.status
		tokens = json.loads(response.read())

		## Query user info to get the user's emaiil address and id
		user_info_request = urllib2.Request(url=UserRelated.user_info_query_url)
		user_info_request.add_header('Authorization', 'Bearer %s' % tokens['access_token'])
		user_info_response = urllib2.urlopen(user_info_request)
		user_info_response = json.loads(user_info_response.read())

		## Store User Info into db
		query_user_info = self.store_auth_data(tokens, user_info_response)

		if query_user_info != None:
			email = query_user_info.email
			google_id = query_user_info.google_id
		else:
			email = user_info_response['email']
			google_id = user_info_response['id']

		return email, google_id

	def refresh_access_token(self, email, google_id, refresh_token):
		## Read client secret file	
		with open(UserRelated.client_secret_file, 'rb') as read_client_secret_file:
			client_secret = json.load(read_client_secret_file)

		parameters = urllib.urlencode({
			'grant_type' : 'refresh_token', 
			'refresh_token' : refresh_token,
			'client_id' : client_secret['web']['client_id'],
			'client_secret' : client_secret['web']['client_secret']
			})

		connection = httplib.HTTPSConnection(UserRelated.auth_token_url)
		connection.request("POST", "", parameters)
		response = connection.getresponse()
		status = response.status
		tokens = json.loads(response.read())
		
		## Update the access token
		self.update_auth_data(email, google_id, tokens)

	def store_auth_data(self, tokens, user_info):
		db_utility = DBUtility()

		query_result = db_utility.search_userinfo(email=user_info['email'], google_id=user_info['id'])
		if query_result == None:
			user_info_key = db_utility.store_userinfo(
				email=user_info['email'], 
				name=user_info['name'], 
		 		picture=user_info['picture'], 
		 		google_id=user_info['id'], 
		 		access_token=tokens['access_token'],
		 		expires_in=tokens['expires_in'],
		 		token_type=tokens['token_type'],
		 		refresh_token=tokens['refresh_token'],
		 		id_token=tokens['id_token'],
		 		register_datetime=datetime.datetime.now(), 
		 		last_login_datetime=datetime.datetime.now(), 
		 		access_token_gen_datetime=datetime.datetime.now())
			
			## Query again to get user data
			query_result = db_utility.search_userinfo(email=user_info['email'], google_id=user_info['id'])

		else:
			query_result.last_loging_datetime = datetime.datetime.now()
			db_utility.update_userinfo(query_result)

		return query_result

	def update_auth_data(self, email, google_id, tokens):
		db_utility = DBUtility()

		query_result = db_utility.search_userinfo(email=email, google_id=google_id)

		query_result.access_token = tokens['access_token']
		query_result.expires_in = tokens['expires_in']
		query_result.access_token_gen_datetime = datetime.datetime.now()
		db_utility.update_userinfo(query_result)


	def get_user_info(self, email, google_id):
		db_utility = DBUtility()
		query_result = db_utility.search_userinfo(email=email, google_id=google_id)

		if (datetime.datetime.now() - query_result.access_token_gen_datetime).total_seconds() > query_result.expires_in:
			## Access toekn is expired, refresh it.
			self.refresh_access_token(email=email, google_id=google_id, refresh_token=query_result.refresh_token)
			query_result = db_utility.search_userinfo(email=email, google_id=google_id)

		return query_result

