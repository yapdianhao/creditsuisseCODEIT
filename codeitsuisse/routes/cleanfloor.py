import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/clean_floor', methods=['POST'])
def evaluateCleanFloor():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data.get("tests");
    answers = dict()
    for i in inputValue:
        answers[i] = cleanFloor(inputValue[i]['floor'])
    #logging.info("My result :{}".format(result))
    return json.dumps({"answers": answers});


def cleanFloor(arr):
    counts = 0
    stack = []
    for i in range(len(arr)):
        if arr[i] > 0:
            stack.append(i)
    curr = 0
    while stack:
        nextDirty = stack.pop()
        if nextDirty > curr:
            while curr < nextDirty:
                if arr[curr] > 0:
                    arr[curr] -= 1
                elif arr[curr]:
                    arr[curr] = 1
                if arr[curr] > 0 and counts != 0:
                    stack.append(curr)
                counts += 1
                curr += 1
        else:
            while curr > nextDirty:
                if arr[curr] > 0:
                    arr[curr] -= 1
                else:
                    arr[curr] 
                    stack.append(curr)
                if arr[curr] > 0 and counts != 0:
                    stack.append(curr)
                counts += 1
                curr -= 1
    return counts



