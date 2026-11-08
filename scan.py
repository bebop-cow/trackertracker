# IN:   url website
# OUT:  printout of trackers
# DONE WHEN: one page load done

# step 1: get_requests(url) - list of requests url

# step 2: for each request,

	# step 3: get_host(url) -> host
	# step 4: is_thirdparty(host, page_host) -> True/False
	# step 5: is_known_tracker(host, trackerlist) -> True/False
	# step 6: counts #counts[host] goes up by 1
#step7: print_counts(counts), sorted, plus total

from urllib.parse import urlparse
import json
TRACKERS = {"doubleclick.net", "demdex.net", "optimizely.com"} 

def get_host(url):
	parsed = urlparse(url)
	if not parsed.hostname:
		return None
	return parsed.hostname

def get_domain(host):
    parts = host.split(".")
    return ".".join(parts[-2:])

def is_third_party(host, page_host):
    domain = get_domain(page_host)
    same_site = host == domain or host.endswith("." + domain)
    return not same_site
		
def is_known_tracker(host, trackerlist):
	return get_domain(host) in trackerlist

# load the HAR json, get the list of entries
har = json.load(open("har.txt"))
entries = har["log"]["entries"]
counts = {}
page_host = "www.cnn.com"
for entry in entries: 
     url = entry["request"]["url"]
     host = get_host(url)
     if host is None:
     	continue
     
     if is_third_party(host, page_host) and is_known_tracker(host, TRACKERS):
         counts[host] = counts.get(host, 0) + 1

def print_counts(counts):
	sort = sorted(counts.items(), key=lambda pair:pair[1], reverse=True)
	for host, n in sort:
		print(f" {host:<28} {n}")
	print(f"Total: {sum(counts.values())} tracker requests")

def main():
	print_counts(counts)
	
if __name__ == '__main__':
	main()
