import requests
import json

# Function to make an HTTP GET request to a given link and parse the JSON response
def request_link(link):
    all_leader_request = requests.get(link)
    content = all_leader_request.content.decode("utf8")
    js = json.loads(content)
    return js
