from db_utility import DBUtility
from youtube_related import Youtube

class Group:
	def get_upload_viedos(self, email, group_name):
		upload_videos = []
		youtube = Youtube()
		db_utility = DBUtility()

		group_details = db_utility.search_user_channel('fetch', email=email, group_name=group_name)

		for group_detail in group_details:
			channel_upload_videos = youtube.get_upload_viedos(group_detail.channel_id, email)
			upload_videos.extend(channel_upload_videos)

		upload_videos = sorted(upload_videos, key=lambda k: k['video_upload_date'], reverse=True) 
		
		return upload_videos

