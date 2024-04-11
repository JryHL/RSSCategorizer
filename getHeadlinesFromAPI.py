import requests
import time

trainingFile = open("training.txt", "a")

query = {'action': 'query', 'list': 'allpages', 'format': 'json', 'aplimit': '500'}

lastContinue = {}
while True:
    thisQuery = query.copy()
    thisQuery.update(lastContinue)
    resp = requests.get("https://en.wikinews.org/w/api.php", params=thisQuery)
    resultJson = resp.json()
    print(resultJson)
    for entry in resultJson["query"]["allpages"]:
        title = entry["title"]
        print(title)
        trainingFile.write(f"{title}\n")
    if 'continue' not in resultJson:
        break
    lastContinue = resultJson['continue']
    time.sleep(0.5) #prevent overloading api

trainingFile.close()