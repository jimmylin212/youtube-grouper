from db_utility import DBUtility
from youtube_related import Youtube

class PlayList:
	def add_videos(self, email, videos):
		youtube_related = Youtube()
		## Check if the playlist exists or not
		playlist_id = self.check_playlist_exisxtence(email)
		for video_id in videos:
			youtube_related.add_video_into_playlist(email, playlist_id, video_id)

		return

	def check_playlist_exisxtence(self, email):
		db_utility = DBUtility()
		youtube_related = Youtube()

		db_playlist_result = db_utility.search_user_playlist(email=email)

		if db_playlist_result == None:
			playlist_id = youtube_related.add_new_playlist(email)
			db_utility.store_user_playlist(email=email, playlist_id=playlist_id)
		else:
			playlist_id = db_playlist_result.playlist_id

		return playlist_id