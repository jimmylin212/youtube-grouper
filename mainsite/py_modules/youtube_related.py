import urllib2, json

class Youtube:
	base_url = 'https://www.googleapis.com/youtube/v3'
	subscriptions_url = '%s/subscriptions?part=snippet&mine=true&maxResults=50' % base_url
	channel_url = '%s/channels/?part=snippet&mine=true' % base_url

	def api_querying(self, query_url, access_token):
		request = urllib2.Request(url=query_url)
		request.add_header('Authorization', 'Bearer %s' % access_token)
		response = urllib2.urlopen(request)
		response = json.loads(response.read())
		return response

	def get_subscriptions(self, user_info):
		all_subscriptions = []
		query_subscriptions = []
		access_token = user_info.access_token

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