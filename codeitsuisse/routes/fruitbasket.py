import logging
import json
import ast
import collections

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/fruitbasket', methods=['POST'])
def evaluateFruitBasket():
    data = ast.literal_eval((request.get_data()).decode('UTF-8'));
    logging.info("data sent for evaluation {}".format(data))
    fruits = dict()
    weight = collections.defaultdict(int)
    weight['maApple'] = 40
    weight['maWatermelon'] = 40
    weight['maBanana'] = 50
    weight['maPineapple'] = 50
    weight['maAvocado'] = 80
    weight['maPomegranate'] = 20
    weight['maRamubutan'] = 45
    total = 0
    for i in data:
        print(i, data[i])
        total += weight[i] * data[i]
    logging.info(fruits)
    return "{}".format(total);



