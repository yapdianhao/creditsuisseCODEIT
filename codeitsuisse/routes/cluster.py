import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/cluster', methods=['POST'])
def evaluateCluster():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    answer = {"answer": cluster(data)}
    logging.info("My result :{}".format(answer))
    return json.dumps(answer);


def cluster(graph):
    infected = []
    visited = [[False for _ in range(len(graph[0]))] for _ in range(len(graph))]
    for i in range(len(graph)):
        for j in range(len(graph[0])):
            if graph[i][j] == '1':
                infected.append((i, j))
    ct = 0
    while infected:
        currX, currY = infected.pop()
        if graph[currX][currY] == '1':
            ct += 1
            dfs(graph, currX, currY, visited)
    return ct


def dfs(graph, x, y, visited):
    if x < 0 or x >= len(graph) or y < 0 or y >= len(graph[0]) or visited[x][y] or graph[x][y] == '*':
        return
    visited[x][y] = True
    graph[x][y] = '/'
    dfs(graph, x - 1, y - 1, visited)
    dfs(graph, x - 1, y, visited)
    dfs(graph, x - 1, y + 1, visited)
    dfs(graph, x, y - 1, visited)
    dfs(graph, x, y + 1, visited)
    dfs(graph, x + 1, y - 1, visited)
    dfs(graph, x, y + 1, visited)
    dfs(graph, x + 1, y + 1, visited)