###################
#	  IMPORTS	  #
################### 
import facebook
import json

#Graph instantiation
graph = facebook.GraphAPI(access_token='EAACzsAEgPn0BAAVSfBTKt1LvMvjiRnLsVL94AXyG4SiSoZAAQ15KV51hFzpkHy1hbOxoihZBM2yPzcHioBYlXUcyUKgd1ZBbKgkIj6reZBXZBBQBM9hgvZALVha7ZANy2IigQqs6tEqfvZAguCnOcYcOA7azDTFb5KOzCDpfSCZAs1KasAiExTxaXRqkpBWBS9cwZD', version='3.1')

####################
#	  API-Calls	   #
####################
#personal information
personal = graph.get_object(id='me', fields='id,name,birthday,gender')

#writing personal data into json-File
with open('personal.json', 'w', encoding='utf-8') as outfile: 
	json.dump(personal, outfile, ensure_ascii=False, indent=3)

#likes
likes = graph.get_connections(id='me', connection_name='likes', fields='name,category,about,genre')
	
#writing like data into json-File
with open('likes.json', 'w', encoding='utf-8') as outfile: 
	json.dump(likes, outfile, ensure_ascii=False, indent=3)
	
#posts
posts = graph.get_connections(id='me', connection_name='posts', fields='message,place,message_tags')

#writing post data into json-File	
with open('posts.json', 'w', encoding='utf-8') as outfile: 
	json.dump(posts, outfile, ensure_ascii=False, indent=3)	

#events
events = graph.get_connections(id='me', connection_name='events', fields='name,description,place,rsvp_status')

#writing event data into json-File
with open('events.json', 'w', encoding='utf-8') as outfile: 
	json.dump(events, outfile, ensure_ascii=False, indent=3)

#groups
groups = graph.get_connections(id='me', connection_name='groups', fields='name,description')

#writing group data into json-File 
with open('groups.json', 'w', encoding='utf-8') as outfile: 
	json.dump(groups, outfile, ensure_ascii=False, indent=3)