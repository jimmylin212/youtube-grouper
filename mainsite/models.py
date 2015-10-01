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

class UserSubscription(ndb.Model):
	email = ndb.StringProperty()
	google_id = ndb.StringProperty()
	