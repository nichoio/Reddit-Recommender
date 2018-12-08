'''Example on how to refresh tokens. An initial token is necessary.'''

import facebook


APP_ID = "app_id"
APP_SECRET = "app_secret"
ACCESS_TOKEN = "access_token"
USER_ID = "user_id"


def personal_data_test(graph, user_id):
    return graph.get_object(
        id=user_id, fields='id,name,address,hometown,age_range,gender')


graph = facebook.GraphAPI(access_token=ACCESS_TOKEN, version='3.1')

print(personal_data_test(graph, USER_ID))

# get new long lived token by using the initial token
long_lived_token = graph.extend_access_token(
    APP_ID, APP_SECRET)['access_token']

graph2 = facebook.GraphAPI(access_token=long_lived_token, version='3.1')

# access same data with new token. Should return the same output
print(personal_data_test(graph2, USER_ID))
