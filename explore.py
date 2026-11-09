import json
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

# ads = data["categories"]["Advertising"]
# print(type(ads))
# print(ads[0])
path = "services.txt"



def get_requests(url):
	urls = []
	with sync_playwright() as p:
		browser = p.chromium.launch()
		page = browser.new_page()
		page.on("request", lambda request: urls.append(request.url))
		page.goto(url, wait_until="networkidle")
		browser.close()
	return urls
 
print(len(get_requests("https://www.cnn.com")))