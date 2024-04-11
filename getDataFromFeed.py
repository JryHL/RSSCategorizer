import feedparser
import sys


feedsFile = open("feeds.txt", "r")
trainingFile = open("training.txt", "a")

for feedTgt in feedsFile:
    NewsFeed = feedparser.parse(feedTgt)
    for entry in NewsFeed.entries:
        result = f"{entry.title}"
        print(result)
        trainingFile.write(f"{result}\n")
    print(f"Wrote {len(NewsFeed.entries)} entries")

trainingFile.close()
feedsFile.close()
