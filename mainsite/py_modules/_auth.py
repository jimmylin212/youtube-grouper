import datetime
from db_utility import DBUtility

class Auth():
	def pass_auth_data(self, tokens, user_info):
		db_utility = DBUtility()

		query_result = db_utility.search_userinfo(email=user_info['email'], google_id=user_info['id'])
		if query_result == None:
			user_info_key = db_utility.store_userinfo(
				email=user_info['email'], name=user_info['name'], 
		 		picture=user_info['picture'], google_id=user_info['id'], access_token=tokens, 
		 		register_datetime=datetime.datetime.now(), last_login_datetime=datetime.datetime.now(), 
		 		access_token_gen_datetime=datetime.datetime.now())
			
			## Query again to get user data
			query_result = db_utility.search_userinfo(email=user_info['email'], google_id=user_info['id'])

		else:
			query_result.last_loging_datetime = datetime.datetime.now()
			db_utility.update_userinfo(query_result)

		return query_result

	


