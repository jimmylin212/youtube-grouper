import logging
from ..models import UserPlayList, AddedVideo, Video
from youtube_related import Youtube

class PlayList:
	def add_videos(self, email, videos):
		youtube_related = Youtube()
		## Check if the playlist exists or not
		playlist_id = self.check_playlist_exisxtence(email)
		for video_id in videos:
			response = youtube_related.add_video_into_playlist(email, playlist_id, video_id)

			if response:
				AddedVideo(email=email, video_id=video_id).put()
				logging.info('%s add video %s into playlist' % (email, video_id))
			else:
				failed_video = Video.query(Video.video_id == video_id).get()
				failed_video.key.delete()
				logging.info('[Error] Adding video %s failed' % video_id)

	def check_playlist_exisxtence(self, email):
		youtube_related = Youtube()

		## Get the user's watch history playlist id
		mine_channel_response = youtube_related.get_mine_channel_details(email)
		for item in mine_channel_response['items']:
			if 'contentDetails' in item:
				watch_history_playlist_id = item['contentDetails']['relatedPlaylists']['watchHistory']

		## Search if the user already have yougroupe playlist
		db_playlist_result = UserPlayList.query(UserPlayList.email == email).get()

		if db_playlist_result == None:
			playlist_id = youtube_related.add_new_playlist(email)
			UserPlayList(email=email, playlist_id=playlist_id, watchhistory_playlist_id=watch_history_playlist_id).put()
			logging.info('%s add new playlist' % email)
		else:
			playlist_id = db_playlist_result.playlist_id

		return playlist_id

	def get_watch_history_playlist_id(self, email):
		db_playlist_result = UserPlayList.query(UserPlayList.email == email).get()
		return db_playlist_result.watchhistory_playlist_id
