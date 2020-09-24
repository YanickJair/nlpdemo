import csv
import collections

import pandas as pd

def load():
    p = '../dataset/yelp.csvdict_itemsdict_items'
    posts = []
    with open(p, newline='') as f:
        spamreader = csv.DictReader(f)
        for row in spamreader:
            posts.append(row["FBPost"])
    return posts
        

""" 
Load Yelp reviews from dataset and ord them by rating
review {
    business_id
    date
    review_id
    stars
    text
    type
    user_id
    cool
    useful
    funny
}
"""
def load_yelp_reviews():
    review_subset = pd.read_csv('/home/yanick/KRAKEN/PIP/NLP/data/Yelp Dataset/yelp.csv')

    reviews_by_rating = collections.defaultdict(list)

    for _, row in review_subset.iterrows():
        reviews_by_rating[row.stars].append(row.to_dict())
    return reviews_by_rating