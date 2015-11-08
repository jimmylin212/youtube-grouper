from ..models import UserPlayList
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
		youtube_related = Youtube()

		db_playlist_result = UserPlayList.query(UserPlayList.email == email).get()

		if db_playlist_result == None:
			playlist_id = youtube_related.add_new_playlist(email)

			UserPlayList(email=email, playlist_id=playlist_id).put()
		else:
			playlist_id = db_playlist_result.playlist_id

		return playlist_id