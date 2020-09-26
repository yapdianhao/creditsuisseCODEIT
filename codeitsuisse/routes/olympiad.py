import logging
import json
import bisect

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/olympiad-of-babylon', methods=['POST'])
def evaluateOlympiad():
    data = request.get_json();
    print(data)
    logging.info("data sent for evaluation {}".format(data))
    books = data.get("books");
    days = data.get("days")
    answer = dict()
    answer["optimalNumberOfBooks"] = olympiad(books, days)
    logging.info("My result :{}".format(answer))
    return jsonify(answer);


def olympiad(books, days):
    books.sort()
    days.sort()
    cumSum = 0
    total = 0
    cumulative = 1
    for i in range(len(books) - 1):
        if not days:
            break
        nextIdx = bisect.bisect_left(days, cumSum)
        if days[nextIdx] - cumSum >= books[i + 1]:
            cumSum += books[i + 1]
            cumulative += 1
        else:
            total += cumulative
            cumSum = books[i + 1]
            days.remove(days[nextIdx])
            cumulative = 1
    return total
