from ..models import UserChannel, Channel
from youtube_related import Youtube

class Subscription:
	def upsert_channel(self, email, channels):
		user_channels = []

		for channel in channels:
			channel_id = channel['channelid']
			## Store channel in UserChannel
			search_user_channel_result = UserChannel.query(UserChannel.email == email, UserChannel.channel_id == channel_id).get()

			if search_user_channel_result == None:
				UserChannel(email=email, channel_id=channel_id, group_name=None).put()

			## Store channel infomation in Channel
			search_channel_result = Channel.query(Channel.channel_id == channel_id).get()

			if search_channel_result == None:
				Channel(channel_id=channel_id, title=channel['title'], thumbnail=channel['thumbnail'], 
						groups=None, upload_playlist_id=None, latest_video_id=None).put()
				

	def get_channel_groups(self, email):
		channel_groups = {}
		no_groups = []

		search_user_channel_results = UserChannel.query(UserChannel.email == email).fetch()

		for search_user_channel_result in search_user_channel_results:
			temp_dict = {}
			group_names = search_user_channel_result.group_name
			channel_id = search_user_channel_result.channel_id
			search_channel_result = Channel.query(Channel.channel_id == channel_id).get()

			if group_names == None:
				temp_dict['title'] = search_channel_result.title
				temp_dict['thumbnail'] = search_channel_result.thumbnail
				temp_dict['channel_id'] = search_channel_result.channel_id
				no_groups.append(temp_dict)
			else:
				for group_name in group_names:
					if group_name not in channel_groups:
						channel_groups[group_name] = []

					temp_dict['title'] = search_channel_result.title
					temp_dict['thumbnail'] = search_channel_result.thumbnail
					temp_dict['channel_id'] = search_channel_result.channel_id
					channel_groups[group_name].append(temp_dict)
		return channel_groups, no_groups

	def add_group(self, email, select_channel_ids, group_names):
		youtube_related = Youtube()

		for select_channel_id in select_channel_ids:
			for group_name in group_names.split(','):
				## Add the group name into UserChannel collection
				search_user_channel_result = UserChannel.query(UserChannel.email == email, 
															   UserChannel.channel_id == select_channel_id).get()
				
				if search_user_channel_result.group_name == None:
					UserChannel(email=email, channel_id=select_channel_id, group_name=[group_name]).put()
				else:
					if group_name not in search_user_channel_result.group_name:
						search_user_channel_result.group_name.append(group_name)
						## Update the new group name
						search_user_channel_result.put()

				## Add the group name into Channel collection
				search_channel_result = Channel.query(Channel.channel_id == select_channel_id).get()
				channel_details = youtube_related.get_channel_details(channel_id=select_channel_id, email=email)
				upload_playlist_id = channel_details['items'][0]['contentDetails']['relatedPlaylists']['uploads']

				if search_channel_result.groups == None:
					search_channel_result.groups = [group_name]
					search_channel_result.upload_playlist_id = upload_playlist_id
					search_channel_result.put()
					
				elif group_name not in search_channel_result.groups:
					search_channel_result.groups.append(group_name)
					search_channel_result.upload_playlist_id = upload_playlist_id
					search_channel_result.put()

