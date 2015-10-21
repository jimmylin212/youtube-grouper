from db_utility import DBUtility
from youtube_related import Youtube

class Group:
	def get_upload_viedos(self, email, group_name):
		upload_videos = []
		youtube = Youtube()
		db_utility = DBUtility()

		group_details = db_utility.search_user_channel('fetch', email=email, group_name=group_name)

		for group_detail in group_details:
			channel_upload_videos = db_utility.search_video(channel_id=group_detail.channel_id)
			for channel_upload_video in channel_upload_videos:
				upload_videos.append({'title' : channel_upload_video.title, 'video_id' : channel_upload_video.video_id,
									  'upload_date' : channel_upload_video.upload_date, 
									  'channel_id' : channel_upload_video.channel_id,
									  'thumbnail' : channel_upload_video.thumbnail})

		upload_videos = sorted(upload_videos, key=lambda k: k['upload_date'], reverse=True)
		return upload_videos

