from optparse import OptionParser
import time
import csv
import fileinput
import sys
import requests
import json

def deliverJoke(prompt, punchline):
    """ Delivers a joke. Print the prompt, then wait for 2 seconds,
    then print the the punchline. """
    print(prompt)
    time.sleep(2)
    print(punchline)

def readHelper(inp):
    """ Based on the input will instruct us what to do.
    If the input is next, then return True.
    If the input is quit, the return False.
    If the input is not readable, then print IDK, and keep
    reading until you get something that you can read."""
    if (inp == 'next'):
        return True
    elif (inp == 'quit'):
        return False
    else:
        print("I don't understand")
        inp = input()
        return readHelper(inp)

def read():
    """ Will read the input and will instruct us what to do next. """
    inp = input()
    return readHelper(inp)

def readCSVFile():
    """ Function that reads a CSV file. and will deliver the joke. """
    csv_reader = csv.reader(fileinput.input(), delimiter=',')
    joke = 0
    for row in csv_reader:
        if (joke == 0):
            joke += 1
            deliverJoke(row[0], row[1])
        else:
            inp_val = read()
            if (inp_val == False):
                sys.exit()
                return
            else:
                deliverJoke(row[0], row[1])

def getRedditJokes():
    """ Get all of the redditJokes from:
    https://www.reddit.com/r/dadjokes.json
    Returns a list of unique dictionaries for each joke.
    """
    redditJokes = []
    r = requests.get('https://www.reddit.com/r/dadjokes.json', headers = {'User-agent': 'your bot 0.1'})
    jokes = r.json()
    for joke in jokes.get('data').get('children'):
        j = {}
        question = joke.get('data').get('title')
        answer = joke.get('data').get('selftext')
        over18 = joke.get('data').get('over_18')
        firstWord = question.split()[0]
        j['question'] = question
        j['answer'] = answer
        if (not over18):
            if (firstWord == 'Why' or firstWord == 'How' or firstWord == 'What'):
                redditJokes.extend([j])
    return redditJokes

def readRedditJokes(reddit):
    """ Takes a list of dictionaries, where each dictionary
    corresponds to a joke. Then, deliver the jokes. """
    n = 0
    for joke in reddit:
        if n == 0:
            n += 1
            deliverJoke(joke.get('question'), joke.get('answer'))
        else:
            inp_val = read()
            if (inp_val == False):
                sys.exit()
                return
            else:
                deliverJoke(joke.get('question'), joke.get('answer'))

def getInputFileName():
    """ Determine whether there is an input csv file that is given.
    If there is no file, then return None,
    otherwise return the name of the file. """
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                      help="write report to FILE", metavar="FILE")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")
    (options, args) = parser.parse_args()
    if len(args) == 0:
        return None
    return args[0]

if (getInputFileName() != None):
    readCSVFile()
else:
    redditJokes = getRedditJokes()
    readRedditJokes(redditJokes)
