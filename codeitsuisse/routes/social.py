import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/social_distancing', methods=['POST'])
def evaluateDP():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    answers = dict()
    for i in data['tests']:
        answers[i] = socialdp(data['tests'][i]['seats'], data['tests'][i]['people'], data['tests'][i]['spaces'])
    logging.info("My result :{}".format(answers))
    return jsonify({"answers": answers})


def socialdp(seats, people, spaces):
    dp = [[0 for _ in range(seats + 1)] for _ in range(people + 1)]
    for i in range(seats + 1):
        dp[0][i] = 1
    for j in range(1, seats + 1):
        dp[1][j] = j
    for i in range(2, people + 1):
        for j in range(1, seats + 1):
            if j < (i - 1) * spaces + i:
                dp[i][j] = 0
            elif j == (i - 1) * spaces + i:
                dp[i][j] = 1
            else:
                if i == 1:
                    print(j)
                dp[i][j] = dp[i][j - 1] + dp[i - 1][j - spaces - 1]
    return dp[-1][-1]




