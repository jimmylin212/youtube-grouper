from ..models import UserChannel, Video
from youtube_related import Youtube

class Group:
	def get_upload_viedos(self, email, group_name):
		upload_videos = []
		youtube = Youtube()

		group_details = UserChannel.query(UserChannel.email == email).fetch()
		for group_detail in group_details:
			if group_detail.group_name == None:
				continue
				
			if group_name in group_detail.group_name:
				## Use the channel id to query video to get the information of the video.
				channel_upload_videos = Video.query(Video.channel_id == group_detail.channel_id)

				for channel_upload_video in channel_upload_videos:
					upload_videos.append({'title' : channel_upload_video.title, 'video_id' : channel_upload_video.video_id,
										  'upload_date' : channel_upload_video.upload_date, 
										  'channel_id' : channel_upload_video.channel_id,
										  'thumbnail' : channel_upload_video.thumbnail})

		upload_videos = sorted(upload_videos, key=lambda k: k['upload_date'], reverse=True)
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

