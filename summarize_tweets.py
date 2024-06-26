#!/bin/python3

import sys
import pandas as pd
import numpy as np

pd.options.mode.chained_assignment = None

def load_df(path_to_file):
    return pd.read_csv(path_to_file, sep='\t')

def summarize_tweet(df, search_term):
    search_df = df[df['text'].str.contains(search_term, case=False, na=False)]

    # Question 1
    # How many tweets were posted containing the term on each day?
    # Not sure what different between ts1 and ts2
    # Use ts1 for simplifity
    search_df['date'] = pd.to_datetime(search_df['ts1']).dt.date
    tweet_count = search_df.groupby('date').count()['id']
    # return tweet_count

    # Question 2
    # How many unique users posted a tweet containing the term?
    # author_id
    user_count = search_df['author_id'].nunique()
    # return user_count

    # Question 3
    # How many likes did tweets containing the term get, on average?
    # like_count
    search_df['like_count'] = pd.to_numeric(search_df['like_count'], errors='coerce').fillna(0).astype(np.int64)
    avg_likes = search_df[search_df['like_count'] >= 0]['like_count'].mean()
    print('avg_likes:', avg_likes)
    # return avg_likes

    # Question 4
    # Where (in terms of place IDs) did the tweets come from?
    # Remove NaN value
    # place_id
    place_id = search_df['place_id'].dropna().unique()
    print('place_id:', place_id)
    # return place_id

    # Question 5
    # What times of day were the tweets posted at?
    # hour
    search_df['hour'] = pd.to_datetime(search_df['ts1']).dt.hour
    # search_df['tod'] = np.NaN
    # Morning: hour >= 6 and < 12
    search_df.loc[(search_df['hour'] >= 6) & (search_df['hour'] < 12), 'tod'] = 'morning'
    # Afternoon: hour >= 12 and < 18
    search_df.loc[(search_df['hour'] >= 12) & (search_df['hour'] < 18), 'tod'] = 'afternoon'
    # Evening: hour >= 18 and <= 23
    search_df.loc[(search_df['hour'] >= 18) & (search_df['hour'] <= 23), 'tod'] = 'evening'
    # Night: hour >= 0 and < 6
    search_df.loc[(search_df['hour'] >= 0) & (search_df['hour'] < 6), 'tod'] = 'night'
    # return search_df[['id','tod']]

    # Question 6
    # Which user posted the most tweets containing the term?
    # author_id
    most_posted_author_id = search_df['author_id'].value_counts().idxmax()
    # return most_posted_author_id

    # Return all answers
    return tweet_count, user_count, avg_likes, place_id, most_posted_author_id, search_df[['id','tod']], most_posted_author_id

def main(path_to_file, search_term):
    df = load_df(path_to_file)
    tweet_count, user_count, avg_likes, place_id, most_posted_author_id, tod_df, most_posted_author_id = summarize_tweet(df, search_term)
    print('tweet_count:', tweet_count)
    print('user_count:', user_count)
    print('avg_likes:', avg_likes)
    print('place_id:', place_id)
    print('tod_df:', tod_df)
    print('most_posted_author_id:', most_posted_author_id)

if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) < 2:
        print('Usage: python summarize_tweets.py full_path_to_csv_file search_terms')
        print('For example: python summarize_tweets.py \'Copy of correct_twitter_202102.tsv\' \'pop music\'')
    else:
        path_to_file = args[0]
        search_term = args[1]

        main(path_to_file, search_term)