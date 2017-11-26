import urllib2,json,pprint

api_key = "thy2rq38b4x72gpd7pehrwsz"
endpoint_prefix = "http://api.walmartlabs.com/v1/items?apiKey="+api_key+"&upc="

if __name__ == "__main__":

    while (True):
        upc = raw_input()
        url = endpoint_prefix + upc
        try:
            response = urllib2.urlopen(url)
            data = json.loads(response.read())
            for item in data["items"]:
                print u"[${0:,.2f}] {1}".format(item["salePrice"],item["name"])
        except urllib2.HTTPError as err:
            if err.code == 403:
                print "HTTP Error 403: Forbidden. Check that your API key is valid."
            if err.code == 404:
                print "HTTP Error 404: Not Found. The UPC code you entered may not be in the database."
            else:
                print err