import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/fruitbasket', methods=['POST'])
def evaluateFruitBasket():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    fruits = dict()
    for i in data:
        fruits[i] = data.get(i)
    logging.info(fruits)
    result = 10000
    logging.info(result)
    return json.dumps(result);



