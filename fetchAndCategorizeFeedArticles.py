import feedparser
import Doc2Vec
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

feedsFile = open("feeds.txt", "r")
entries = []

# fetch RSS entries
for feedTgt in feedsFile:
    NewsFeed = feedparser.parse(feedTgt)
    for entry in NewsFeed.entries:
        title = str(entry.title)
        link = str(entry.link)
        entries.append((title, link))

feedsFile.close()
# initialize Doc2Vec
Doc2Vec.prepare_system()

# Find embeddings
vectors = []
for entry in entries:
    vector = Doc2Vec.getInferredVector(entry[0])
    vectors.append(vector)

# Use KMeans to cluster
xvals = []
costs = []
labels = []
for numClusters in range(1, len(vectors)):
    kmeans = KMeans(n_clusters=numClusters, n_init=1, max_iter=50).fit(vectors)
    
    costs.append(kmeans.inertia_)
    xvals.append(numClusters)
    print(f"Found kmeans for {numClusters} clusters with cost {kmeans.inertia_}")
    #TODO: Find better elbow point
    if kmeans.inertia_ < (costs[0]/7):
        labels = kmeans.labels_
        break



categoriesDict = {}
for label in labels:
    categoriesDict[label] = []

for idx, label in enumerate(labels):
    categoriesDict[label].append(entries[idx])

resultsFile = open("results.txt", "w")
for idx, category in enumerate(categoriesDict.values()):
    resultsFile.write(f"Articles in category {idx}:\n")
    for article in category:
        resultsFile.write(f"{article[0]}\n")
    resultsFile.write("\n")

resultsFile.close()
print("Wrote to results file")
plt.plot(xvals, costs)
plt.xlabel("Number of clusters")
plt.ylabel("Cost")
plt.show()