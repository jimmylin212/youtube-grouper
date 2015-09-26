from ..models import UserInfo

class DBUtility:
	def store_userinfo(self, **kwargs):
		stored_user_info = UserInfo(**kwargs)
		user_info_key = stored_user_info.put()
		return user_info_key

	def search_userinfo(self, **kwargs):
		return UserInfo.query(*(getattr(UserInfo, k)==v for (k,v) in kwargs.items())).get()

	def update_userinfo(self, update_document):
		update_document.put()
