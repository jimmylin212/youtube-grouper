from ..models import UserInfo, Channel, UserChannel, UserPlayList

class DBUtility:
	def store_userinfo(self, **kwargs):
		store_document = UserInfo(**kwargs)
		user_info_key = store_document.put()
		return user_info_key

	def search_userinfo(self, **kwargs):
		return UserInfo.query(*(getattr(UserInfo, k)==v for (k,v) in kwargs.items())).get()

	def update_userinfo(self, update_document):
		update_document.put()

	def store_user_channel(self, **kwargs):
		store_document = UserChannel(**kwargs)
		store_key = store_document.put()
		return store_key

	def search_user_channel(self, method, **kwargs):
		if method == 'get':
			return UserChannel.query(*(getattr(UserChannel, k)==v for (k,v) in kwargs.items())).get()
		elif method == 'fetch':
			return UserChannel.query(*(getattr(UserChannel, k)==v for (k,v) in kwargs.items())).fetch()

	def update_user_channel(self, update_document):
		update_document.put()
		return

	def store_channel(self, **kwargs):
		store_document = Channel(**kwargs)
		store_key = store_document.put()
		return store_key

	def search_channel(self, **kwargs):
		return Channel.query(*(getattr(Channel, k)==v for (k,v) in kwargs.items())).get()

	def update_channel(self, update_document):
		update_document.put()
		return

	def search_user_playlist(self, **kwargs):
		return UserPlayList.query(*(getattr(UserPlayList, k)==v for (k,v) in kwargs.items())).get()

	def store_user_playlist(self, **kwargs):
		store_document = UserPlayList(**kwargs)
		store_key = store_document.put()
		return store_key
