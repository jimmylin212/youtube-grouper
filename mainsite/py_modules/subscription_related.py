from db_utility import DBUtility

class Subscription:
	def upsert_subscriptions(self, email, all_subscriptions):
		db_utility = DBUtility()

		## Search in subscription to see if there is the data for the user
		search_result = db_utility.search_subscription(email=email)

		if search_result == None:
			## Create new data for the user
			insert_channels = {}
			for subscription in all_subscriptions:
				channelid = subscription['channelid']

				insert_channels[channelid] = {}
				insert_channels[channelid]['channel_id'] = channelid
				insert_channels[channelid]['channel_title'] = subscription['title']
				insert_channels[channelid]['channel_thumbnail'] = subscription['thumbnail']
				insert_channels[channelid]['channel_group'] = "No Group"

			db_utility.store_subscription(email=email, channels=insert_channels, all_groups=[])
			return insert_channels
		else:
			## Check the subscription to see is there any new subscription
			return search_result.channels

	def create_group_based_dict(self, channels):
		grouped_channels = {}

		for channel in channels:
			group_name = channels[channel]['channel_group']
			
			if group_name not in grouped_channels:
				grouped_channels[group_name] = []

			grouped_channels[group_name].append(channels[channel])

		return grouped_channels

	def add_group_name(self, email, select_channel_ids, group_name):
		db_utility = DBUtility()

		## Search in subscription to see if there is the data for the user
		search_result = db_utility.search_subscription(email=email)

		for select_channel_id in select_channel_ids:
			search_result.channels[select_channel_id]['channel_group'] = group_name

			if group_name not in search_result.all_groups:
				search_result.all_groups.append(group_name)

		db_utility.update_subscription(search_result)
