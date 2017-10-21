import logging
from ..models import UserChannel, Video, AddedVideo
from youtube_related import Youtube
from google.appengine.api import memcache

class Group:
	def get_upload_viedos(self, email, group_name):
		youtube = Youtube()

		upload_videos = memcache.get('%s_%s' % (email, group_name))

		if upload_videos == None:
			upload_videos = []	
			## Get the channels of the select group
			group_details = UserChannel.query(UserChannel.email == email).fetch()
			for group_detail in group_details:
				if group_detail.group_name == None:
					continue

				if group_name in group_detail.group_name:
					## Use the channel id to query video to get the information of the video.
					channel_upload_videos = Video.query(Video.channel_id == group_detail.channel_id)
					for channel_upload_video in channel_upload_videos:
						## Checkt if the video is already in playlist
						added_video_result = AddedVideo.query(AddedVideo.email == email,
															AddedVideo.video_id == channel_upload_video.video_id).get()
						if added_video_result == None:
							upload_videos.append({'title' : channel_upload_video.title, 'video_id' : channel_upload_video.video_id,
												'upload_date' : channel_upload_video.upload_date,
												'channel_id' : channel_upload_video.channel_id,
												'thumbnail' : channel_upload_video.thumbnail})

			memcache.add(key='%s_%s' % (email, group_name), value=upload_videos, time=43200)

		upload_videos = sorted(upload_videos, key=lambda k: k['upload_date'], reverse=True)
		upload_videos = [upload_videos[x:x+4] for x in xrange(0, len(upload_videos), 4)]

		return upload_videos

	def remove_group(self, email, group_name):
		group_details = UserChannel.query(UserChannel.email == email).fetch()

		for group_detail in group_details:
			if group_detail.group_name == None:
				continue

			if group_name in group_detail.group_name:
				user_channel_detail = UserChannel.query(UserChannel.channel_id == group_detail.channel_id,
												  	    UserChannel.email == email).get()
				user_channel_detail.group_name.remove(group_name)
				if user_channel_detail.group_name == []:
					user_channel_detail.group_name = None

				user_channel_detail.put()

		logging.info('%s remove group %s' % (email, group_name))
