import logging
import json
import collections

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/supermarket', methods=['POST'])
def evaluateMarket():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    ans = dict()
    ans['answers'] = dict()
    for i in data['tests']:
        maze = data['tests'][i]['maze']
        start = data['tests'][i]['start']
        end = data['tests'][i]['end']
        startY, startX = start
        endY, endX = end
        ans['answers'][i] = bfs(maze, startX, startY, endX, endY)
    logging.info("My result :{}".format(ans))
    return jsonify(ans);


def bfs(grid, startX, startY, endX, endY):
    q = collections.deque()
    directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    q.append((startX, startY, 1))
    visited = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]
    while q:
        currX, currY, ctr = q.popleft()
        visited[currX][currY] = True
        if currX == endX and currY == endY:
            return ctr
        for direction in directions:
            newX, newY = currX + direction[0], currY + direction[1]
            if newX < 0 or newX >= len(grid) or newY < 0 or newY >= len(grid[0]) or visited[newX][newY] or grid[newX][newY] == 1:
                continue
            q.append((newX, newY, ctr + 1))
    return -1



