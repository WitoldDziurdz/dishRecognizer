# pip3 install --upgrade google-api-python-client

from apiclient.discovery import build
import pprint

# api key
api_key = "AIzaSyAEz3e4ve7aFU3iui-FfYXqXF2uP4oFK8I"

service = build('customsearch', 'v1', developerKey=api_key)
request = service.cse().list(
    q='butterfly',
    cx='015941098266592620936:divui1smer0',
    searchType='image',
    num=3,pyt
    safe= 'off'
)
response = request.execute()

# print results
if not 'items' in response:
    print('No result !!\nres is: {}'.format(response))
else:
    for item in response['items']:
        print('{}:\n\t{}'.format(item['title'], item['link']))
