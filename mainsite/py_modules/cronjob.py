import urllib2, datetime, re
import xml.etree.ElementTree as etree
from ..models import Channel, Video
from youtube_related import Youtube

class CronJob:
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


