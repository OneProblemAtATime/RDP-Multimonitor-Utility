import urllib.request
import json

def printResults(data):
    theJSON = json.loads(data)
    if "title" in theJSON["metadata"]:
        print(theJSON["metadata"]["title"])
    
    count = theJSON["metadata"]["count"]
    print(count)

    for i in theJSON["features"]:
        print(i["properties"]["place"])
    print("--------------Above 4")
    for i in theJSON["features"]:
        if i["properties"]["mag"] > 4:
            print(i["properties"]["place"])
    print("--------------Felt")
    for i in theJSON["features"]:
        feltReports = i["properties"]["felt"]
        if feltReports != None:
            if feltReports > 0:
                print(i["properties"]["place"], feltReports)


def main():
    urlData = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson"
    weburl = urllib.request.urlopen(urlData)
    print(weburl.getcode())

    if (weburl.getcode() == 200):
        data = weburl.read()
        printResults(data)
    else:
        print("Server eror: ", weburl.getcode())


if __name__ == "__main__":
    main()