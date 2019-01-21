import facebook

def get_u_id(access_token):
	graph = facebook.GraphAPI(access_token=access_token, version='3.1')
	data = graph.get_object(id='me', fields='id')
	return data['id']