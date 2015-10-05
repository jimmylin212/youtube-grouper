from ..models import UserInfo, UserSubscription, Channels

class DBUtility:
	def store_userinfo(self, **kwargs):
		stored_user_info = UserInfo(**kwargs)
		user_info_key = stored_user_info.put()
		return user_info_key

	def search_userinfo(self, **kwargs):
		return UserInfo.query(*(getattr(UserInfo, k)==v for (k,v) in kwargs.items())).get()

	def update_userinfo(self, update_document):
		update_document.put()

	def store_subscription(self, **kwargs):
		store_user_subscription = UserSubscription(**kwargs)
		user_subscription_key = store_user_subscription.put()
		return user_subscription_key

	def search_subscription(self, **kwargs):
		return UserSubscription.query(*(getattr(UserSubscription, k)==v for (k,v) in kwargs.items())).get()

	def update_subscription(self, update_document):
		update_document.put()
		return
