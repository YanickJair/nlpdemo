import csv

def load():
    p = '../dataset/datasets_73978_166769_fb_sentiment.csv'
    posts = []
    with open(p, newline='') as f:
        spamreader = csv.DictReader(f)
        for row in spamreader:
            posts.append(row["FBPost"])
    return posts
        