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
	group_name = ndb.StringProperty()

class Channel(ndb.Model):
	channel_id = ndb.StringProperty()
	channel_title = ndb.StringProperty()
	channel_thumbnail = ndb.StringProperty()

class UserPlayList(ndb.Model):
	email = ndb.StringProperty()
	playlist_id = ndb.StringProperty()