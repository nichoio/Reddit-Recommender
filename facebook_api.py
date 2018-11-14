import facebook 

graph = facebook.GraphAPI(access_token="EAAFB8eOiQXsBAAygETK6tOcRI1fXKRlZBZAs3gEzvNrYOa1EH4l7NDYLG9RxhFpU9MUOhInyb2N0HxfO1flvACyIcm58ieOjhYJWmuv9XFFZC0aMjYbUw94YcG1bqjFt52qgFeKPYcxlywZAR9ly59ZBIWdrcElcaR87sg42XbgZDZD", version="3.1")

post = graph.get_object(id='me', fields='id,name')

print(post['id'] + ' ' + post['name'])

