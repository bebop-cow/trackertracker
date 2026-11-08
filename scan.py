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

import json
from urllib.parse import urlparse
 
 
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
 
 
def is_known_tracker(host, trackers):
    return get_domain(host) in trackers
 
 
def load_trackers(path):
    trackers = {}
    data = json.load(open(path))
    for name,category in data["categories"].items():
        for company in category:
            for inner in company.values():
                for value in inner.values():
                    if isinstance(value, list):
                        for domain in value:
                        	trackers.setdefault(domain, set()).add(name)
    return trackers
 
 
def print_counts(counts,cats):
    ranked = sorted(counts.items(), key=lambda pair: pair[1], reverse=True)
    for host, n in ranked:
        print(f" {host:<32} {n:<4} {', '.join(sorted(cats[host]))}")
    
    print(f"Total: {sum(counts.values())} tracker requests")
 
 
def main():
    trackers = load_trackers("services.txt")
    har = json.load(open("har.txt"))
    entries = har["log"]["entries"]
    page_host = "www.cnn.com"
    counts = {}
    cats = {}
    for entry in entries:
        url = entry["request"]["url"]
        host = get_host(url)
        if host is None:
            continue
        if is_third_party(host, page_host) and is_known_tracker(host, trackers):
            counts[host] = counts.get(host, 0) + 1
            cats[host] = trackers[get_domain(host)]
 
    print_counts(counts, cats)
    
 
 
if __name__ == "__main__":
    main()