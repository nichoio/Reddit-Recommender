import facebook
import json


def fetch_and_write(type_, fields):
    '''fetch drom Facebook and API and write selected fields to new JSON file'''
    data = graph.get_connections(id='me', connection_name=type_, fields=fields)
    with open('{}.json'.format(type_), 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)


# Graph instantiation
graph = facebook.GraphAPI(access_token='access_token', version='3.1')


# personal information - different request structure, hence use custom code
personal = graph.get_object(id='me', fields='id,name,birthday,gender')
with open('personal.json', 'w', encoding='utf-8') as outfile:
    json.dump(personal, outfile, ensure_ascii=False, indent=4)

fetch_and_write('likes', 'name,category,about,genre')
fetch_and_write('posts', 'message,place,message_tags')
fetch_and_write('events', 'name,description,place,rsvp_status')
fetch_and_write('groups', 'name,description')
