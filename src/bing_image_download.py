import requests
import shutil

subscription_key = '9f4746d3f2de467a9b6e816810d4c383'
assert subscription_key

search_url = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
search_term = "butterfly"

offset = 0
count = 20

# build request
headers = {"Ocp-Apim-Subscription-Key": subscription_key}
params = {"count": count, "offset": offset, "q": search_term}
response = requests.get(search_url, headers=headers, params=params)
response.raise_for_status()
search_results = response.json()

# get urls from response
content_url = []
for img in search_results["value"]:
    content_url.append(img["contentUrl"])

# download files
n = 1
for url in content_url:
    name = 'picture' + str(n) + '.jpg'
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open('./pictures/' + name, 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)
    n += 1
