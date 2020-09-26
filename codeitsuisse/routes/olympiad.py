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
    totalTime = sum(days)
    dp = [[[0, 0] for _ in range(totalTime + 1)] for _ in range(len(books))]
    for j in range(totalTime + 1):
        if j >= books[0]:
            dp[0][j] = [1, books[0]]
    for i in range(1, len(books)):
        for j in range(totalTime + 1):
            chosen = max(dp[i - 1][j], dp[i][j - 1], key = lambda x: x[0])
            dp[i][j] = chosen[:]
            if chosen[1] + books[i] <= j and chosen[0] <= i:
                dp[i][j][0] += 1
                dp[i][j][1] += books[i]
    #print(dp)
    return dp[-1][-1][0]
