from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import os
import urllib.request as urllib

# input: search_terms = ['searchterm1, searchterm2, searchterm3, ...'] - list of strings
def scrape_google_img(search_terms):
    browser = webdriver.Chrome()
    for term in search_terms:
        results = get_urls_google(term, browser)
        download_imgs(term, results)
    browser.close()

# input: searchterm - string, img_data_list (tuple of 2 strings) - (url, imgtype)
# used by scrape_google_img
def download_imgs(search_term, img_data_list):
    # fake a browser
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36'}
    total = 0
    succes = 0
    if not os.path.exists(search_term):
        os.mkdir(search_term)
    for url, imgtype in img_data_list:
        total = total + 1
        print("[INFO] Total Count:", total)
        print("[INFO] Succsessful Count:", succes)
        print("[INFO] URL:", url)
        img = url
        try:
            req = urllib.Request(img, headers=headers)
            raw_img = urllib.urlopen(req, timeout=10).read()
            File = open(os.path.join(search_term , search_term + "_" + str(total) + "." + imgtype), "wb")
            File.write(raw_img)
            File.close()
            succes = succes + 1
        except Exception as e:
            print("[ERROR] Can't get image.", e)

# input: search_term - string, browser - selenium browser object, example: selenium.webdriver.Chrome()
# used by scrape_google_img
def get_urls_google(search_term, browser):
    url = "https://www.google.pl/search?q=" + search_term + "&source=lnms&tbm=isch"
    browser.get(url)

    # go down with browser
    for _ in range(500):
        browser.execute_script("window.scrollBy(0,10000)")
        try:
            show_more_btn = browser.find_element_by_id("smb")
            if show_more_btn.is_displayed():
                show_more_btn.click()
        except Exception as e:
            print("[ERROR] Exception:", e.__traceback__)

    list_of_elements = browser.find_elements_by_xpath('//div[contains(@class,"rg_meta")]')

    # get tuples list (url, img_type)
    image_data_list = []
    for x in list_of_elements:
        url_imgtype_tuple = json.loads(x.get_attribute('innerHTML'))["ou"], json.loads(x.get_attribute('innerHTML'))["ity"]
        image_data_list.append(url_imgtype_tuple)

    return image_data_list
