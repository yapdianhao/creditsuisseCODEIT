import logging
import json
import math

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/salad-spree', methods=['POST'])
def evaluateSaladSpree():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    salads = data.get("number_of_salads");
    streets = data.get("salad_prices_street_map")
    result = buySalad(salads, streets)
    logging.info("result:{}".format(result))
    return json.dumps(result);


def buySalad(target, streets):
    ans = 0
    money = math.inf
    for street in streets:
        money = min(money, getMoneyForStreet(target, street))
    return 0 if money == math.inf else money


def getMoneyForStreet(target, street):
    money = []
    ans = math.inf
    for i in range(len(street)):
        if street[i] == 'X':
            money = []
        else:
            money.append(int(street[i]))
            if len(money) == target:
                ans = min(ans, sum(money))
                money = money[1:]
    return ans

