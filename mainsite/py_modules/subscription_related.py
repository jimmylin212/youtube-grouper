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
			search_channel_result = db_utility.search_channel(channel_id=channel_id)

			if search_channel_result == None:
				db_utility.store_channel(
					channel_id=channel_id, channel_title=channel['title'],
					channel_thumbnail=channel['thumbnail'])

	def get_channel_groups(self, email):
		channel_groups = {}
		db_utility = DBUtility()

		search_user_channel_results = db_utility.search_user_channel('fetch', email=email)

		for search_user_channel_result in search_user_channel_results:
			group_name = search_user_channel_result.group_name
			channel_id = search_user_channel_result.channel_id
			search_channel_result = db_utility.search_channel(channel_id=channel_id)

			if group_name not in channel_groups:
				channel_groups[group_name] = []

			channel_groups[group_name].append(search_channel_result)

		return channel_groups

	def add_group(self, email, select_channel_ids, group_name):
		db_utility = DBUtility()

		for select_channel_id in select_channel_ids:
			search_result = db_utility.search_user_channel('get', email=email, channel_id=select_channel_id)
			if search_result == None:
				db_utility.store_user_channel(email=email, channel_id=select_channel_id, group_name=group_name)
			else:
				search_result.group_name = group_name
				db_utility.update_user_channel(search_result)

