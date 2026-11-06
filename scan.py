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
		
