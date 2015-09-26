from django.db import models
from google.appengine.ext import ndb

class UserInfo(ndb.Model):
	email = ndb.StringProperty()
	name = ndb.StringProperty()
	picture = ndb.StringProperty()
	google_id = ndb.StringProperty()
	access_token = ndb.JsonProperty()
	register_datetime = ndb.DateTimeProperty()
	last_login_datetime = ndb.DateTimeProperty()
	access_token_gen_datetime = ndb.DateTimeProperty()
