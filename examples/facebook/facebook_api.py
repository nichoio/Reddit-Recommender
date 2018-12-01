import facebook
import json


graph = facebook.GraphAPI(access_token='access_token', version='3.1')

#personal information
personal = graph.get_object(id='me', fields='id,name,address,hometown,age_range,gender')

#writing personal data into json-File
with open('personal.json', 'w') as outfile: 
	json.dump(personal, outfile, ensure_ascii=False)

#likes
likes = graph.get_connections(id='me', connection_name='likes', fields='name,category,about,genre')
	
#writing like data into json-File
with open('likes.json', 'w') as outfile: 
	json.dump(likes, outfile, ensure_ascii=False)
	
#posts
posts = graph.get_connections(id='me', connection_name='posts', fields='message,place,message_tags')

#writing post data into json-File	
with open('posts.json', 'w') as outfile: 
	json.dump(posts, outfile, ensure_ascii=False)	

#events
events = graph.get_connections(id='me', connection_name='events', fields='name,description,place,rsvp_status')

#writing event data into json-File
with open('events.json', 'w') as outfile: 
	json.dump(events, outfile, ensure_ascii=False)

#groups
groups = graph.get_connections(id='me', connection_name='groups', fields='name,description')

#writing group data into json-File 
with open('groups.json', 'w') as outfile: 
	json.dump(groups, outfile, ensure_ascii=False)