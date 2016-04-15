from __future__ import division
import json
import sys
import matplotlib.pyplot as plt
import datetime
import time
import csv
from collections import Counter
from collections import OrderedDict

__author__ = 'Venkata Naga Sai Dheeraj Gadhiraju and Maaz Siddiqui'
### This project is done in a group of two people "Venkata Naga Sai Dheeraj Gadhiraju and Maaz Siddiqui".
### We divided the project in a way that first two tasks were solved by Venkata Naga Sai Dheeraj Gadhiraju
### and the tasks third and fourth were solved by Maaz Siddiqui and the fifth task was completed colaboratively".


def read_stocktwits():
    with open("C:\Users\dheeraj\Google Drive\Data Science\INFS 774\Project2\BAC.json") as json_file:
        json_data = json.load(json_file)

    tweet = []

    for item in json_data:
        item_list = []
        body = ''.join(ch.encode('ascii', 'ignore').lower() if (ch.isalnum() or ch == ' ') else ' ' for ch in item['body'])
        item_list.append(body)
        fmt = "%Y-%m-%d %H:%M:%S"
        date = datetime.datetime.fromtimestamp(float(item['created_at']['$date']) / 1000.).strftime(fmt)
        item_list.append(date)
        if item['entities']['sentiment'] is None:
            sentiment = "Unknown"
        else:
            sentiment = item['entities']['sentiment']['basic']
        item_list.append(str(sentiment))
        tweet.append(item_list)

    # Write to output to file

    with open("C:\Users\dheeraj\Google Drive\Data Science\INFS 774\Project2\BAC.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(tweet)


def sentiment_analysis():

    tweet = []

    with open('C:\Users\dheeraj\Google Drive\Data Science\INFS 774\Project2\positive_words.txt', 'r') as filename:
        positive_words = filename.readlines()
        positive_words = map(lambda s: s.strip(), positive_words)

    with open('C:\\Users\\dheeraj\\Google Drive\\Data Science\\INFS 774\\Project2\\negative_words.txt', 'r') as filename:
        negative_words = filename.readlines()
        negative_words = map(lambda s: s.strip(), negative_words)

    with open("C:\Users\dheeraj\Google Drive\Data Science\INFS 774\Project2\BAC.csv", "rb") as csv_file:
        input_file = csv.reader(csv_file)
        for row in input_file:
            item = []
            if row[2] == 'Unknown':
                positive_count = len(list(set(positive_words).intersection(row[0].split())))
                negative_count = len(list(set(negative_words).intersection(row[0].split())))
                if positive_count == negative_count or (positive_count == 0 and negative_count == 0):
                    sentiment = 'Neutral'
                elif positive_count > negative_count:
                    sentiment = 'Bullish'
                else:
                    sentiment = 'Bearish'
                item.append(row[1])
                item.append(sentiment)
            else:
                item.append(row[1])
                item.append(row[2])

            tweet.append(item)

    with open("C:\Users\dheeraj\Google Drive\Data Science\INFS 774\Project2\BAC2.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(tweet)


def get_sentiment_dates(start_date, end_date):

    start_date = datetime.datetime(*time.strptime(start_date, "%Y-%m-%d")[0:3])
    end_date = datetime.datetime(*time.strptime(end_date, "%Y-%m-%d")[0:3])

    positive_list = []
    negative_list = []
    neutral_list = []

    with open("C:\Users\dheeraj\Google Drive\Data Science\INFS 774\Project2\BAC2.csv", "rb") as csv_file:
        input_file = csv.reader(csv_file)
        for row in input_file:
            tweet_date = row[0]
            tweet_date = datetime.datetime(*time.strptime(tweet_date, "%Y-%m-%d %H:%M:%S")[0:3])
            tweet_type = row[1].strip()
            if tweet_date >= start_date and tweet_date <= end_date:
                if tweet_type == 'Neutral':
                    neutral_list.append(tweet_date)
                elif tweet_type == 'Bullish':
                    positive_list.append(tweet_date)
                else:
                    negative_list.append(tweet_date)

    positive_dict = {}
    negative_dict = {}
    neutral_dict = {}

    positive_dict = dict(Counter(positive_list))
    negative_dict = dict(Counter(negative_list))
    neutral_dict = dict(Counter(neutral_list))
    print [positive_dict, negative_dict, neutral_dict]
    return [positive_dict, negative_dict, neutral_dict]


def drawing_pie(start_date, end_date):

    (positive_dict, negative_dict, neutral_dict) = get_sentiment_dates(start_date, end_date)
    positive_tweets_count = sum(positive_dict.values())
    negative_tweets_count = sum(negative_dict.values())
    neutral_tweets_count = sum(neutral_dict.values())

    total_tweets_count = positive_tweets_count + negative_tweets_count + neutral_tweets_count
    positive_tweets_perc = positive_tweets_count/total_tweets_count*100
    negative_tweets_perc = negative_tweets_count/total_tweets_count*100
    neutral_tweets_perc = neutral_tweets_count/total_tweets_count*100

    overall_sentiment = ''

    if positive_tweets_count > negative_tweets_count and positive_tweets_count > neutral_tweets_count:
        overall_sentiment = 'Positive'
    elif negative_tweets_count > positive_tweets_count and negative_tweets_count > neutral_tweets_count:
        overall_sentiment = 'Negative'
    elif neutral_tweets_count > positive_tweets_count and neutral_tweets_count > negative_tweets_count:
        overall_sentiment = 'Neutral'
    elif positive_tweets_count == negative_tweets_count:
        overall_sentiment = 'Neutral'
    elif positive_tweets_count == neutral_tweets_count and positive_tweets_count > negative_tweets_count:
        overall_sentiment = 'Positive'
    elif negative_tweets_count == neutral_tweets_count and negative_tweets_count > positive_tweets_count:
        overall_sentiment = 'Negative'

    labels = 'Positive', 'Negative', 'Neutral'
    sizes = [positive_tweets_perc, negative_tweets_perc, neutral_tweets_perc]
    colors = ['blue', 'green', 'red']
    figure_title = 'Sentiment is ' + overall_sentiment

    plt.pie(sizes, labels=labels, colors=colors,
        autopct='%1.0f%%', shadow=True)
    plt.axis('equal')
    plt.text(0, 1.1, figure_title,
         horizontalalignment='right',
         fontsize=15)
    plt.show()
    return


def drawing_lines(start_date, end_date):

    (positive_dict, negative_dict, neutral_dict) = get_sentiment_dates(start_date, end_date)
    positive_dict = OrderedDict(sorted(positive_dict.items(), key=lambda t: t[0]))
    pos_keys = positive_dict.keys()
    pos_vals = positive_dict.values()
    pos_keys = pos_keys[-30:]  # get the last 30 days

    negative_dict = OrderedDict(sorted(negative_dict.items(), key=lambda t: t[0]))
    neg_keys = negative_dict.keys()
    neg_vals = negative_dict.values()
    neg_keys = neg_keys[-30:]  # get the last 30 days

    neutral_dict = OrderedDict(sorted(neutral_dict.items(), key=lambda t: t[0]))
    neu_keys = neutral_dict.keys()
    neu_vals = neutral_dict.values()
    neu_keys = neu_keys[-30:]  # get the last 30 days

    figure_title = 'Sentiment between ' + start_date + ' and ' + end_date
    fig, ax = plt.subplots()
    ax.plot(pos_keys, pos_vals, 'o-', label='Positive')
    ax.plot(neg_keys, neg_vals, 'o-', label='Negative')
    ax.plot(neu_keys, neu_vals, 'o-', label='Neutral')
    fig.autofmt_xdate()
    plt.legend(shadow=True, fancybox=True)
    plt.title(figure_title)
    plt.show()

    return


def main():
    read_stocktwits()  # output: BAC.csv
    sentiment_analysis()  # output BAC2.csv
    get_sentiment_dates('2013-01-02', '2013-01-31')#output:[{datetime.date(2013, 1, 26): 4, datetime.date(2013, 1, 24): 44, datetime.date(2013, 1, 6): 31, datetime.date(2013, 1, 4): 63, datetime.date(2013, 1, 2): 108, datetime.date(2013, 1, 23): 41, datetime.date(2013, 1, 21): 4, datetime.date(2013, 1, 14): 25, datetime.date(2013, 1, 19): 6, datetime.date(2013, 1, 12): 11, datetime.date(2013, 1, 17): 153, datetime.date(2013, 1, 10): 75, datetime.date(2013, 1, 31): 19, datetime.date(2013, 1, 8): 66, datetime.date(2013, 1, 29): 18, datetime.date(2013, 1, 27): 6, datetime.date(2013, 1, 25): 25, datetime.date(2013, 1, 7): 79, datetime.date(2013, 1, 5): 27, datetime.date(2013, 1, 3): 60, datetime.date(2013, 1, 22): 44, datetime.date(2013, 1, 15): 45, datetime.date(2013, 1, 20): 7, datetime.date(2013, 1, 13): 14, datetime.date(2013, 1, 18): 59, datetime.date(2013, 1, 11): 52, datetime.date(2013, 1, 16): 66, datetime.date(2013, 1, 9): 137, datetime.date(2013, 1, 30): 19, datetime.date(2013, 1, 28): 23}, {datetime.date(2013, 1, 26): 3, datetime.date(2013, 1, 24): 20, datetime.date(2013, 1, 6): 5, datetime.date(2013, 1, 4): 24, datetime.date(2013, 1, 2): 27, datetime.date(2013, 1, 23): 18, datetime.date(2013, 1, 21): 2, datetime.date(2013, 1, 14): 18, datetime.date(2013, 1, 19): 1, datetime.date(2013, 1, 12): 2, datetime.date(2013, 1, 17): 70, datetime.date(2013, 1, 10): 37, datetime.date(2013, 1, 31): 10, datetime.date(2013, 1, 8): 39, datetime.date(2013, 1, 29): 11, datetime.date(2013, 1, 27): 1, datetime.date(2013, 1, 25): 4, datetime.date(2013, 1, 7): 33, datetime.date(2013, 1, 5): 6, datetime.date(2013, 1, 3): 8, datetime.date(2013, 1, 22): 24, datetime.date(2013, 1, 15): 21, datetime.date(2013, 1, 20): 4, datetime.date(2013, 1, 13): 4, datetime.date(2013, 1, 18): 36, datetime.date(2013, 1, 11): 17, datetime.date(2013, 1, 16): 22, datetime.date(2013, 1, 9): 124, datetime.date(2013, 1, 30): 12, datetime.date(2013, 1, 28): 6}, {datetime.date(2013, 1, 26): 4, datetime.date(2013, 1, 24): 15, datetime.date(2013, 1, 6): 9, datetime.date(2013, 1, 4): 40, datetime.date(2013, 1, 2): 63, datetime.date(2013, 1, 23): 34, datetime.date(2013, 1, 21): 4, datetime.date(2013, 1, 14): 19, datetime.date(2013, 1, 19): 6, datetime.date(2013, 1, 12): 12, datetime.date(2013, 1, 17): 148, datetime.date(2013, 1, 10): 51, datetime.date(2013, 1, 31): 13, datetime.date(2013, 1, 8): 49, datetime.date(2013, 1, 29): 18, datetime.date(2013, 1, 27): 3, datetime.date(2013, 1, 25): 15, datetime.date(2013, 1, 7): 77, datetime.date(2013, 1, 5): 7, datetime.date(2013, 1, 3): 40, datetime.date(2013, 1, 22): 37, datetime.date(2013, 1, 15): 21, datetime.date(2013, 1, 20): 4, datetime.date(2013, 1, 13): 6, datetime.date(2013, 1, 18): 48, datetime.date(2013, 1, 11): 40, datetime.date(2013, 1, 16): 49, datetime.date(2013, 1, 9): 104, datetime.date(2013, 1, 30): 26, datetime.date(2013, 1, 28): 15}]
     #As you can see in the output, I used datetime.date objects as keys of a dictionary. You can also do this, you can use date strings as keys.
    drawing_pie('2013-01-02', '2013-01-31') #output: pie_sentiment.png - you can see a graph in a pop-up window. you don't need to save the graph
    drawing_lines('2013-01-02', '2013-01-31') # output: lines_sentiment.png
    return


if __name__ == '__main__':
    main()
