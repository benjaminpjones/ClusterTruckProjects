import urllib2,json
import threading
from collections import deque

# We will hold a queue of responses to ensure successive scans are printed in order
class response_holder:
    def __init__(self):
        self.complete = False
        self.error = None
        self.response = None

# Print all responses that have been received from Walmart
def print_complete(q):
    while q and q[0].complete:
        curr_rh = q.popleft()
        response = curr_rh.response
        if response == None:
            err = curr_rh.error
            if err == None:
                print "Unknown Error Occured."
            elif err.code == 403:
                print "HTTP Error 403: Forbidden. Check that your API key is valid."
            elif err.code == 404:
                print "HTTP Error 404: Not Found. The UPC code you entered may not be in the database."
            else:
                print err
            continue
            
        data = json.loads(response.read())
        for item in data["items"]:
            print u"[${0:,.2f}] {1}".format(item["salePrice"],item["name"])
    return        

def request_info(url, curr_rh,q):
    try:
        curr_rh.response = urllib2.urlopen(url)
    except urllib2.HTTPError as err:
        curr_rh.error = err
        print err
    curr_rh.complete = True
    print_complete(q)
    return

if __name__ == "__main__":

    api_key = "thy2rq38b4x72gpd7pehrwsz"
    endpoint_prefix = "http://api.walmartlabs.com/v1/items?apiKey="+api_key+"&upc="

    response_queue = deque()

    while (True):
        upc = raw_input()
        url = endpoint_prefix + upc
        curr_rh = response_holder()
        response_queue.append(curr_rh)
        t = threading.Thread(target=request_info,args=(url,curr_rh,response_queue))
        t.start()
        