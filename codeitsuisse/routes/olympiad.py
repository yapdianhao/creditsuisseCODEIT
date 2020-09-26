import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/olympiad-of-babylon', methods=['POST'])
def evaluateOlympiad():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    books = data.get("books");
    days = data.get("days")
    answer = dict()
    answer["optimalNumberOfBooks"] = olympiad(books, days)
    logging.info("My result :{}".format(answer))
    return jsonify(answer);


def olympiad(books, days):
    books.sort()
    days.sort(reverse = True)
    added = set()
    for day in days:
        twoPointer(books, day, added)
    return len(added)

def twoPointer(books, day, added):
    left = 0
    right = len(books) - 1
    while left <= right:
        if left == right:
            if books[left] not in added:
                added.add(books[left])
            return
        elif books[left] + books[right] <= day:
            if books[left] not in added and books[right] not in added:
                added.add(books[left])
                added.add(books[right])
                break
            elif books[left] in added:
                left += 1
            elif books[right] in added:
                right -= 1
        elif books[left] + books[right] > day:
            if books[right] in added:
                right -= 1
            elif books[left] in added:
                left += 1
            else:
                right -= 1
