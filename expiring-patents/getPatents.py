# Creating this as it's own module is probably not a best practice, but I've done it anyways.

import requests
import sqlite3
import os
from random import randint


def exists_in_table(patent, cursor):
    cursor.execute('SELECT 1 FROM Tweets WHERE num={}'.format(patent))

    if cursor.fetchone() is not None:
        return True
    else:
        return False


def patent_list(date1, date2):
    if not os.path.isfile('tweets.db'):
        db = sqlite3.connect('tweets.db')
        cursor = db.cursor()

        cursor.execute('CREATE TABLE Tweets(num INT, name TEXT)')
    else:
        db = sqlite3.connect('tweets.db')
    cursor = db.cursor()

    results = requests.get(('http://www.patentsview.org/api/patents/query?q={{%22_and%22:[{{%22_gte%22:{{'
                            '%22patent_date%22:%22{0}%22}}}},{{%22_lte%22:{{%22patent_date%22:%22{'
                            '1}%22}}}}]}}').format(date1, date2))
    json = results.json()
    count = json['count']

    selection = 0
    move_on = False
    visited = []
    while len(visited) != count and not move_on:
        selection = randint(0, count-1)
        patent_number = json['patents'][selection]['patent_number']
        patent_name = json['patents'][selection]['patent_title']

        if not exists_in_table(patent_number, cursor):
            query = "INSERT INTO Tweets VALUES({0}, '{1}')".format(patent_number, patent_name)
            cursor.execute(query)
            db.commit()
            move_on = True
        if patent_number not in visited:
            visited.append(patent_number)

    if len(visited) == count:
        print('No more untweeted results found!')
        exit(1)

    tweet = ""
    chars_left = 140

    link = 'http://patents.google.com/patent/US{}'.format(patent_number)

    tweet = tweet + link + ' - '
    chars_left = chars_left - len(link) - 3

    if chars_left > len(patent_name):
        tweet = tweet + patent_name
    else:
        tweet = tweet + patent_name[:chars_left-3]
        tweet = tweet + '...'

    db.close()
    return tweet
