from db_utility import DBUtility
from youtube_related import Youtube

class PlayList:
	def add_videos(self, email, videos):
		db_utility = DBUtility()
		youtube_related = Youtube()

		user_playlist_result = db_utility.search_user_playlist(email=email)

		if user_playlist_result == None:
			user_playlists = youtube_related.add_new_playlist(email)

		b = c
		return