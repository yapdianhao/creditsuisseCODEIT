import logging
import json
import collections

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
    q = collections.deque()
    total = 0
    start = 0
    if arr[0] > 0:
        q.append(1)
        q.append(0)
    while q:
        curr = q.popleft()
        #print(curr)
        if arr[curr] == 0:
            arr[curr] += 1
            q.append(curr)
        elif arr[curr] > 0:
            arr[curr] -= 1
            if arr[curr] > 0:
                q.append(curr)
        total += 1
        start = curr
    for i in range(start, len(arr)):
        if arr[i] > 0:
            q.append(i)
    while q:
        nextIdx = q.popleft()
        if arr[nextIdx] == 0:
            continue
        while start < nextIdx:
            tempq = collections.deque()
            start += 1
            total += 1
            if arr[start] == 0:
                arr[start] += 1
            elif arr[start] > 0:
                arr[start] -= 1
            if arr[start] > 0:
                tempq.append(start)
                tempq.append(start + 1)
            while tempq:
                curr = tempq.popleft()
                if arr[curr] == 0:
                    q.append(curr)
                elif arr[curr] > 0:
                    arr[curr] -= 1
                    if arr[curr] > 0:
                        tempq.append(curr)
                total += 1
                start = curr
    return total



