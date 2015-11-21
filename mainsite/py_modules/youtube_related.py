import urllib, urllib2, json, datetime, httplib, urlparse
from user_related import UserRelated

class Youtube:
	base_url = 'https://www.googleapis.com/youtube/v3'
	subscriptions_url = '%s/subscriptions?part=snippet&mine=true&maxResults=50' % base_url
	videos_url = '%s/videos?' % base_url
	channel_url = '%s/channels?' % base_url
	playlist_url = '%s/playlists?' % base_url
	playlistitem_url = '%s/playlistItems?' % base_url

	def api_querying(self, query_url, access_token, query_data=None):
		request = urllib2.Request(url=query_url, data=query_data)
		if query_data != None:
			request.add_header('Content-Type', 'application/json')

		request.add_header('Authorization', 'Bearer %s' % access_token)
		response = urllib2.urlopen(request)
		response = json.loads(response.read())
		return response

	def api_querying_method(self, method, query_domain, query_path, access_token):
		headers = {'Authorization' : 'Bearer %s' % access_token}

		connection = httplib.HTTPSConnection(query_domain)
		connection.request(method, query_path, '', headers) 
		response = connection.getresponse()
		return response.read()

	def query_dict_2_para(self, query_dict):
		return '&'.join(['{}={}'.format(key, value) for key, value in query_dict.iteritems()])

	def query_video(self, email, video_id):
		## Get access token from userinfo
		user_related = UserRelated()
		query_user_info = user_related.get_user_info(email=email)
		access_token = query_user_info.access_token

		query_para = {'part' : 'snippet', 'id' : video_id}
		query_para = self.query_dict_2_para(query_para)
		query_url = "%s%s" % (Youtube.videos_url, query_para)
		response = self.api_querying(query_url, access_token)

		return response

	def get_subscriptions(self, email):
		all_subscriptions = []
		query_subscriptions = []

		## Get access token from userinfo
		user_related = UserRelated()
		query_user_info = user_related.get_user_info(email=email)
		access_token = query_user_info.access_token

		query_url = Youtube.subscriptions_url
		while True:
			response = self.api_querying(query_url, access_token)
			query_subscriptions.extend(response['items'])
			if 'nextPageToken' in response:
				query_url = '%s&pageToken=%s' % (Youtube.subscriptions_url, response['nextPageToken'])
			else:
				break

		for subscription in query_subscriptions:
			temp_dict = {}
			temp_dict['thumbnail'] = subscription['snippet']['thumbnails']['default']['url']
			temp_dict['title'] = subscription['snippet']['title']
			temp_dict['channelid'] = subscription['snippet']['resourceId']['channelId']
			all_subscriptions.append(temp_dict)

		return all_subscriptions

	def get_channel_details(self, channel_id, email):
		user_related = UserRelated()
		## Get access token from userinfo
		query_user_info = user_related.get_user_info(email=email)
		access_token = query_user_info.access_token

		## Query and get the upload video playlist id
		query_para = {'part' : 'contentDetails', 'id' : channel_id}
		query_para = self.query_dict_2_para(query_para)
		query_url = "%s%s" % (Youtube.channel_url, query_para)
		response = self.api_querying(query_url, access_token)

		return response

	def get_mine_channel_details(self, email):
		user_related = UserRelated()
		## Get access token from userinfo
		query_user_info = user_related.get_user_info(email=email)
		access_token = query_user_info.access_token

		query_para = {'part' : 'contentDetails', 'mine' : 'true'}
		query_para = self.query_dict_2_para(query_para)
		query_url = "%s%s" % (Youtube.channel_url, query_para)
		response = self.api_querying(query_url, access_token)

		return response

	def get_upload_viedos(self, playlist_id, email):
		upload_videos = []
		user_related = UserRelated()
		show_days_delta = 14

		## Get access token from userinfo
		query_user_info = user_related.get_user_info(email=email)
		access_token = query_user_info.access_token

		## Get the video in the upload play list
		query_para = {'part' : 'contentDetails', 'playlistId' : playlist_id, 'maxResults' : 50}
		query_para = self.query_dict_2_para(query_para)
		query_url = "%s%s" % (Youtube.playlistitem_url, query_para)
		response = self.api_querying(query_url, access_token)
		channel_upload_videos = response['items']

		for channel_upload_video in channel_upload_videos:
			temp_dict = {}
			video_id = channel_upload_video['contentDetails']['videoId']
			query_para = {'part' : 'snippet', 'id' : video_id}
			query_para = self.query_dict_2_para(query_para)
			query_url = "%s%s" % (Youtube.videos_url, query_para)
			response = self.api_querying(query_url, access_token)

			video_upload_date = response['items'][0]['snippet']['publishedAt'].split('T')[0]
			if (datetime.datetime.now() - datetime.datetime.strptime(video_upload_date, '%Y-%m-%d')).days > show_days_delta:
				break
			else:
				temp_dict['video_id'] = video_id
				temp_dict['video_upload_date'] = video_upload_date
				temp_dict['video_thumbnail'] = response['items'][0]['snippet']['thumbnails']['default']['url']
				temp_dict['video_title'] = response['items'][0]['snippet']['title']
				temp_dict['channel_title'] = response['items'][0]['snippet']['channelTitle']

				upload_videos.append(temp_dict)
		return upload_videos

	def add_new_playlist(self, email):
		## Get access token from userinfo
		user_related = UserRelated()
		query_user_info = user_related.get_user_info(email=email)
		access_token = query_user_info.access_token

		## Create new playlist
		default_playlist_title = 'YouGroupe'
		default_playlist_description = 'Playlist for YouGroupe'

		query_para = {'part' : 'snippet,status'}
		query_para = self.query_dict_2_para(query_para)
		query_data = {'snippet' : {'title' : default_playlist_title, 'description' : default_playlist_description},
					  'status' : {'privacyStatus' : 'public'}}
		query_data = json.dumps(query_data)
		query_url = "%s%s" % (Youtube.playlist_url, query_para)
		response = self.api_querying(query_url=query_url, access_token=access_token, query_data=query_data)

		return response['id']

	def add_video_into_playlist(self, email, playlist_id, video_id):
		## Get access token from userinfo
		user_related = UserRelated()
		query_user_info = user_related.get_user_info(email=email)
		access_token = query_user_info.access_token

		query_para = {'part' : 'snippet'}
		query_para = self.query_dict_2_para(query_para)
		query_data = {'snippet' : {'playlistId' : playlist_id, 
								   'resourceId' : {'videoId' : video_id, 'kind' : 'youtube#video'}}}
		query_data = json.dumps(query_data)
		query_url = "%s%s" % (Youtube.playlistitem_url, query_para)
		response = self.api_querying(query_url=query_url, access_token=access_token, query_data=query_data)

		return response

	def remove_all_from_playlist(self, email, playlist_id):
		## Get access token from userinfo
		user_related = UserRelated()
		query_user_info = user_related.get_user_info(email=email)
		access_token = query_user_info.access_token

		yougroupe_playlist_videos = [] 
		query_para = {'part' : 'snippet', 'maxResults' : '50', 'playlistId' : playlist_id}
		query_para = self.query_dict_2_para(query_para)
		while True:
			query_url = "%s%s" % (Youtube.playlistitem_url, query_para)
			response = self.api_querying(query_url=query_url, access_token=access_token)
			yougroupe_playlist_videos.extend(response['items'])
			if 'nextPageToken' in response:
				query_para = {'part' : 'snippet', 'maxResults' : '50',
							  'playlistId' : playlist_id, 'pageToken' : response['nextPageToken']}
				query_para = self.query_dict_2_para(query_para)
			else:
				break

		for video_detail in yougroupe_playlist_videos:
			playlist_item_id = video_detail['id']
			video_id = video_detail['snippet']['resourceId']['videoId']

			query_para = {'id' : playlist_item_id}
			query_para = self.query_dict_2_para(query_para)
			query_url = "%s%s" % (Youtube.playlistitem_url, query_para)
			parsed_query_url = urlparse.urlparse(query_url)

			query_domain = parsed_query_url.netloc
			query_path_para = '%s?%s' % (parsed_query_url.path, parsed_query_url.query)
			response = self.api_querying_method("DELETE", query_domain, query_path_para, access_token)

	def remove_watched_from_playlist(self, email, playlist_id, watch_history_playlist_id):
		## Get access token from userinfo
		user_related = UserRelated()
		query_user_info = user_related.get_user_info(email=email)
		access_token = query_user_info.access_token

		yougroupe_playlist_videos = [] 
		query_para = {'part' : 'snippet', 'maxResults' : '50', 'playlistId' : playlist_id}
		query_para = self.query_dict_2_para(query_para)
		while True:
			query_url = "%s%s" % (Youtube.playlistitem_url, query_para)
			response = self.api_querying(query_url=query_url, access_token=access_token)
			yougroupe_playlist_videos.extend(response['items'])
			if 'nextPageToken' in response:
				query_para['nextPageToken'] = response['nextPageToken']
				query_para = self.query_dict_2_para(query_para)
			else:
				break

		for video_detail in yougroupe_playlist_videos:
			playlist_item_id = video_detail['id']
			video_id = video_detail['snippet']['resourceId']['videoId']
			
			## Query to see if the video in watch history		
			query_para = {'part' : 'contentDetails', 'videoId' : video_id, 'playlistId' : watch_history_playlist_id}
			query_para = self.query_dict_2_para(query_para)
			query_url = "%s%s" % (Youtube.playlistitem_url, query_para)
			response = self.api_querying(query_url=query_url, access_token=access_token)

			if response['pageInfo']['totalResults'] == 1:
				query_para = {'id' : playlist_item_id}
				query_para = self.query_dict_2_para(query_para)
				query_url = "%s%s" % (Youtube.playlistitem_url, query_para)

				query_domain = parsed_query_url.netloc
				query_path_para = '%s?%s' % (parsed_query_url.path, parsed_query_url.query)
				response = self.api_querying_method("DELETE", query_domain, query_path_para, access_token)
