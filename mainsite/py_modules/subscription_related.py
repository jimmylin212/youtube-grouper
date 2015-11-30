import datetime, urllib2, re
from ..models import UserChannel, Channel, Video
from youtube_related import Youtube

class Subscription:
	def upsert_channel(self, email, channels):
		new_channel_count = 0
		removed_channel_count = 0
		query_channels = []

		## Add the newly subscribe channel
		for channel in channels:
			channel_id = channel['channelid']
			query_channels.append(channel_id)
			## Store channel in UserChannel
			search_user_channel_result = UserChannel.query(UserChannel.email == email, UserChannel.channel_id == channel_id).get()

			if search_user_channel_result == None:
				UserChannel(email=email, channel_id=channel_id, group_name=None).put()

			## Store channel infomation in Channel
			search_channel_result = Channel.query(Channel.channel_id == channel_id).get()

			if search_channel_result == None:
				Channel(channel_id=channel_id, title=channel['title'], thumbnail=channel['thumbnail'],
						groups=None, upload_playlist_id=None, latest_video_id=None).put()
				new_channel_count = new_channel_count + 1

		## Remove the unsubscribe channel
		db_channels = UserChannel.query(UserChannel.email == email).fetch()
		for db_channel in db_channels:
			channel_id = db_channel.channel_id
			if channel_id not in query_channels:
				search_user_channel_result = UserChannel.query(UserChannel.email == email, UserChannel.channel_id == channel_id).get()
				search_user_channel_result.key.delete()
				removed_channel_count = removed_channel_count + 1

		return new_channel_count, removed_channel_count

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
					search_user_channel_result.group_name = [group_name]
					search_user_channel_result.put()
				else:
					if group_name not in search_user_channel_result.group_name:
						search_user_channel_result.group_name.append(group_name)
						## Update the new group name
						search_user_channel_result.put()

				## Add the group name into Channel collection
				search_channel_result = Channel.query(Channel.channel_id == select_channel_id).get()
				channel_details = youtube_related.get_channel_details(channel_id=select_channel_id, email=email)
				upload_playlist_id = channel_details['items'][0]['contentDetails']['relatedPlaylists']['uploads']

				## If there is no group for the channel, then add. If there is group, then append
				if search_channel_result.groups == None:
					search_channel_result.groups = [group_name]
					search_channel_result.upload_playlist_id = upload_playlist_id
					search_channel_result.put()
					## Get the latest uploaded video
					self.parse_latest_videos(select_channel_id)

				elif group_name not in search_channel_result.groups:
					search_channel_result.groups.append(group_name)
					search_channel_result.upload_playlist_id = upload_playlist_id
					search_channel_result.put()

	def parse_latest_videos(self, channel_id):
		add_videos = []
		day_delta = 4
		feed_url_prefix = r'https://www.youtube.com/feeds/videos.xml?channel_id='
		day_stop = (datetime.date.today() - datetime.timedelta(days=day_delta)).strftime('%Y-%m-%d')

		entry_ptn = re.compile('\<entry\>(.*?)\<\/entry\>', re.DOTALL)
		video_id_ptn = re.compile('\<yt\:videoId\>(.*?)\<\/yt\:videoId\>')
		title_ptn = re.compile('\<title\>(.*?)\<\/title\>')
		upload_date_ptn = re.compile('\<published\>(.*?)\<\/published\>')
		thumbnail_ptn = re.compile('media\:thumbnail url\=\"(.*?)\"')

		feed_url = '%s%s' % (feed_url_prefix, channel_id)
		page = urllib2.urlopen(feed_url)
		page_source = page.read()
		entries = entry_ptn.findall(page_source)

		for entry in entries:
			video_id = video_id_ptn.findall(entry)[0]
			title = title_ptn.findall(entry)[0]
			thumbnail = thumbnail_ptn.findall(entry)[0]
			upload_date = upload_date_ptn.findall(entry)[0].split('T')[0]

			if upload_date == day_stop:
				break

			if video_id != None and title != None and upload_date != None:
				upload_date = datetime.datetime.strptime(upload_date, '%Y-%m-%d')
				## Store new uploaded video
				store_doc = Video(channel_id=channel_id, title=title, video_id=video_id,
								  upload_date=upload_date, thumbnail=thumbnail)
				store_doc.put()
				add_videos.append(video_id)
