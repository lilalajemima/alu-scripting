#!/usr/bin/python3
"""A script that counts the number of occurrences of list of words
in a given subreddit."""

import requests


headers = {'User-Agent': 'MyAPI/0.0.1'}


def count_words(subreddit, word_list, after="", hot_list=[]):
    """print the sorted count of word_list."""

    subreddit_url = "https://reddit.com/r/{}/hot.json".format(subreddit)

    parameters = {'limit': 100, 'after': after}
    response = requests.get(subreddit_url, headers=headers, params=parameters)

    if response.status_code == 200:

        json_data = response.json()
        if (json_data.get('data').get('dist') == 0):
            return
        for child in json_data.get('data').get('children'):
            title = child.get('data').get('title')
            hot_list.append(title)
        after = json_data.get('data').get('after')
        if after is not None:
            return count_words(subreddit, word_list,
                               after=after, hot_list=hot_list)
        else:
            counter = {}
            for word in word_list:
                word = word.lower()
                if word not in counter.keys():
                    counter[word] = 0
                else:
                    counter[word] += 1
            for title in hot_list:
                title_list = title.lower().split(' ')
                for word in counter.keys():
                    search_word = "{}".format(word)
                    if search_word in title_list:
                        counter[word] += 1
            sorted_counter = dict(
                sorted(counter.items(),
                       key=lambda item: item[1], reverse=True))
            for key, value in sorted_counter.items():
                if value > 0:
                    print("{}: {}".format(key, value))

    else:
        return
