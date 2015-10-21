from db_utility import DBUtility
from youtube_related import Youtube

class Subscription:
	def upsert_channel(self, email, channels):
		user_channels = []
		db_utility = DBUtility()

		for channel in channels:
			channel_id = channel['channelid']
			## Store channel in UserChannel
			search_user_channel_result = db_utility.search_user_channel(
				'get', email=email, channel_id=channel_id)

			if search_user_channel_result == None:
				db_utility.store_user_channel(
					email=email, channel_id=channel_id, group_name="No Group")

			## Store channel infomation in Channel
			search_channel_result = db_utility.search_channel('==', channel_id=channel_id)

			if search_channel_result == None:
				db_utility.store_channel(
					channel_id=channel_id, title=channel['title'], thumbnail=channel['thumbnail'], 
					groups=None, upload_playlist_id=None, latest_video_id=None)

	def get_channel_groups(self, email):
		channel_groups = {}
		db_utility = DBUtility()

		search_user_channel_results = db_utility.search_user_channel('fetch', email=email)

		for search_user_channel_result in search_user_channel_results:
			temp_dict = {}
			group_name = search_user_channel_result.group_name
			channel_id = search_user_channel_result.channel_id
			search_channel_result = db_utility.search_channel('==', channel_id=channel_id)

			if group_name not in channel_groups:
				channel_groups[group_name] = []

			temp_dict['title'] = search_channel_result.title
			temp_dict['thumbnail'] = search_channel_result.thumbnail
			temp_dict['channel_id'] = search_channel_result.channel_id
			channel_groups[group_name].append(temp_dict)

		return channel_groups

	def add_group(self, email, select_channel_ids, group_name):
		db_utility = DBUtility()
		youtube_related = Youtube()

		for select_channel_id in select_channel_ids:
			## Add the group name into UserChannel collection
			search_user_channel_result = db_utility.search_user_channel('get', email=email, channel_id=select_channel_id)
			if search_user_channel_result == None:
				db_utility.store_user_channel(email=email, channel_id=select_channel_id, group_name=group_name)
			else:
				search_user_channel_result.group_name = group_name
				db_utility.update_user_channel(search_user_channel_result)

			## Add the group name into Channel collection
			search_channel_result = db_utility.search_channel('==', channel_id=select_channel_id)
			channel_details = youtube_related.get_channel_details(channel_id=select_channel_id, email=email)
			upload_playlist_id = channel_details['items'][0]['contentDetails']['relatedPlaylists']['uploads']

			if search_channel_result.groups == None:
				search_channel_result.groups = [group_name]
				search_channel_result.upload_playlist_id = upload_playlist_id
				db_utility.update_channel(search_channel_result)
			elif group_name not in search_channel_result.channel_groups:
				search_channel_result.groups.append(group_name)
				search_channel_result.upload_playlist_id = upload_playlist_id
				db_utility.update_channel(search_channel_result)

