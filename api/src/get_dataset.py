import csv
import os
import collections

import pandas as pd

def load():
    p = ''
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
def load_yelp_reviews(start=0, end=10):
    review_subset = pd.read_csv(os.getcwd() + '/dataset/yelp.csv')

    reviews = [] # collections.defaultdict(list)
    pages = int(len(review_subset) / 10)

    for _, row in review_subset[start:end].iterrows():
        reviews.append({
            "review_id": row.review_id,
            "text": row.text
        })
        # reviews_by_rating[row.stars].append(row.to_dict())
    return reviews, pages