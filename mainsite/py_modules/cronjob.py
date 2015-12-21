import urllib2, datetime, re, logging
import xml.etree.ElementTree as etree
from ..models import Channel, Video, AddedVideo
from youtube_related import Youtube

class CronJob:
	query_email = r'jimmylin212@gmail.com'
	feed_url_prefix = r'https://www.youtube.com/feeds/videos.xml?channel_id='

	def get_daily_uplaod_videos(self):
		day_before = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
		entry_ptn = re.compile('\<entry\>(.*?)\<\/entry\>', re.DOTALL)
		video_id_ptn = re.compile('\<yt\:videoId\>(.*?)\<\/yt\:videoId\>')
		title_ptn = re.compile('\<title\>(.*?)\<\/title\>')
		upload_date_ptn = re.compile('\<published\>(.*?)\<\/published\>')
		thumbnail_ptn = re.compile('media\:thumbnail url\=\"(.*?)\"')

		youtube_related = Youtube()

		## Get the channel with tags
		channels = Channel.query(Channel.groups != None).fetch()

		for channel in channels:
			channel_id = channel.channel_id
			logging.info('Parsing channel %s' % channel_id)
			feed_url = '%s%s' % (CronJob.feed_url_prefix, channel.channel_id)
			try:
				page = urllib2.urlopen(feed_url)
			except urllib2.HTTPError:
				continue

			page_source = page.read()
			entries = entry_ptn.findall(page_source)
			for entry in entries:
				video_id = video_id_ptn.findall(entry)[0]
				title = title_ptn.findall(entry)[0]
				thumbnail = thumbnail_ptn.findall(entry)[0]
				upload_date = upload_date_ptn.findall(entry)[0].split('T')[0]

				if video_id != None and title != None and upload_date != None and upload_date == day_before:

					upload_date = datetime.datetime.strptime(upload_date, '%Y-%m-%d')
					## Store new uploaded video
					store_doc = Video(channel_id=channel_id, title=title, video_id=video_id,
									  upload_date=upload_date, thumbnail=thumbnail)
					store_doc.put()
					logging.info('[Success] Store video %s into db' % video_id)
				else:
					logging.info('[Failed] Store video %s into db, title = %s, upload_date = %s, day_before = %s' % (video_id, title, upload_date, day_before))

	def daily_check_video_status(self):
		youtube_related = Youtube()

		video_details = Video.query().fetch()
		for video_detail in video_details:
			logging.info('Daily check video status query %s' % video_detail.video_id)
			response = youtube_related.query_video(CronJob.query_email, video_detail.video_id)
			if response['pageInfo']['totalResults'] == 0:
				video_detail.key.delete()
				logging.info('Remove %s from db' % video_detail.video_id)

	def daily_check_channel_status(self):
		youtube_related = Youtube()
		return

	def perge_old_videos(self):
		delete_video_count = 0
		old_video_days = 14
		old_video_date = datetime.date.today() - datetime.timedelta(days=old_video_days)
		old_videos = Video.query(Video.upload_date < old_video_date).fetch()
		for old_video in old_videos:
			add_video = AddedVideo.query(AddedVideo.video_id == old_video.video_id).get()
			if add_video == None:
				old_video.key.delete()
				delete_video_count = delete_video_count + 1

		logging.info('Remove %s old videos' % delete_video_count)
