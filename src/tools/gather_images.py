from requests import exceptions
import requests
import google_img
from threading import Thread
from to_png import to_jpeg

API_KEY = "33e6e287bbb143818c1898325cb471f4"


def get_bing_urls(term, api_key):
	MAX_RESULTS = 5000
	GROUP_SIZE = 50

	URL = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"

	EXCEPTIONS = {
		IOError, FileNotFoundError,
		exceptions.RequestException,
		exceptions.HTTPError,
		exceptions.ConnectionError,
		exceptions.Timeout
	}

	headers = {"Ocp-Apim-Subscription-Key": api_key}
	params = {"q": term, "offset": 0, "count": GROUP_SIZE}

	# make the search
	search = requests.get(URL, headers=headers, params=params)
	search.raise_for_status()

	# get the results
	results = search.json()
	estNumResults = min(results["totalEstimatedMatches"], MAX_RESULTS)

	total = 0
	list_of_urls = []

	for offset in range(0, estNumResults, GROUP_SIZE):
		params["offset"] = offset
		search = requests.get(URL, headers=headers, params=params)
		search.raise_for_status()
		results = search.json()
		for v in results["value"]:
			try:
				element = v["contentUrl"], v["contentUrl"][v["contentUrl"].rfind("."):]
				list_of_urls.append(element)
			except Exception as e:
				if type(e) in EXCEPTIONS:
					print("[INFO] skipping: {}".format(v["contentUrl"]))
					continue
			total += 1

	return list_of_urls


def scrape_bing_img(term):
	list_of_urls = get_bing_urls(term, API_KEY)
	google_img.download_imgs(term, list_of_urls)


def download_imgs(list_of_terms):
	print("start")
	for term in list_of_terms:
		thread_bing = Thread(target=scrape_bing_img, args=(term,))
		thread_bing.start()
		thread_google = Thread(target=google_img.scrape_google_img, args=(term,))
		thread_google.start()

		thread_bing.join()
		thread_google.join()

	print("end")


list_of_dishes = ['flaczki']
download_imgs(list_of_dishes)
for dir in list_of_dishes:
	to_jpeg(dir)
