import facebook


graph = facebook.GraphAPI(access_token='mytoken', version='3.1')

post = graph.get_object(id='me', fields='id,name')

print(post['id'] + ' ' + post['name'])

# print likes of the user related to the access_token
likes = graph.get_connections(id='me', connection_name='likes')
print(likes)
