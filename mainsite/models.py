from django.db import models
from google.appengine.ext import ndb

class UserInfo(ndb.Model):
	email = ndb.StringProperty()
	name = ndb.StringProperty()
	picture = ndb.StringProperty()
	google_id = ndb.StringProperty()
	access_token = ndb.StringProperty()
	expires_in = ndb.IntegerProperty()
	token_type = ndb.StringProperty()
	refresh_token = ndb.StringProperty()
	id_token = ndb.StringProperty()
	register_datetime = ndb.DateTimeProperty()
	last_login_datetime = ndb.DateTimeProperty()
	access_token_gen_datetime = ndb.DateTimeProperty()

class UserChannel(ndb.Model):
	email = ndb.StringProperty()
	channel_id = ndb.StringProperty()
	group_name = ndb.JsonProperty(indexed=True)

class Channel(ndb.Model):
	channel_id = ndb.StringProperty()
	title = ndb.StringProperty()
	thumbnail = ndb.StringProperty()
	groups = ndb.JsonProperty(indexed=True)
	upload_playlist_id = ndb.StringProperty()
	latest_video_id = ndb.StringProperty()

class UserPlayList(ndb.Model):
	email = ndb.StringProperty()
	playlist_id = ndb.StringProperty()

class Video(ndb.Model):
	channel_id = ndb.StringProperty()
	video_id = ndb.StringProperty()
	upload_date = ndb.DateProperty()
	title = ndb.StringProperty()
	thumbnail = ndb.StringProperty()