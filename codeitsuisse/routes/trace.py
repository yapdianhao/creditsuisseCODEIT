import logging
import json
import collections
import math

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/contact_trace', methods=['POST'])
def evaluateTrace():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    infected = data["infected"]
    origin = data["origin"]
    clusters = data["cluster"]
    ans = getAns(infected, origin, clusters)
    return jsonify(ans);


def getAns(infected, origin, clusters):
    neighbours = collections.defaultdict(list)
    idMap = dict()
    gnomeMap = []
    start = 0
    idMap[infected["name"]] = start
    gnomeMap.append(infected)
    start += 1
    idMap[origin['name']] = start
    gnomeMap.append(origin)
    for cluster in clusters:
        start += 1
        idMap[cluster['name']] = start
        gnomeMap.append(cluster)
    compareClusterInfected(idMap, gnomeMap, neighbours, clusters, infected, origin)
    compareWithinCluster(idMap, gnomeMap, neighbours, clusters, infected, origin)
    ans = []
    dfs(0, ans, neighbours, idMap, gnomeMap, '')
    return ans

    

def compareClusterInfected(idMap, gnomeMap, neighbours, clusters, infected, origin):
    score = (math.inf, -1)
    for cluster in clusters:
        currScore = getScore(infected, cluster)
        if score[0] > currScore[0]:
            score = currScore
    for cluster in clusters:
        currScore = getScore(infected, cluster)
        if score[0] == currScore[0]:
            neighbours[idMap[infected['name']]].append((idMap[cluster['name']], currScore[1]))
    scoreWithOrigin = getScore(infected, origin)
    if score[0] >= scoreWithOrigin[0]:
        neighbours[idMap[infected['name']]].append((idMap[origin['name']], scoreWithOrigin[1]))


def compareWithinCluster(idMap, gnomeMap, neighbours, clusters, infected, origin):
    for i in range(len(clusters)):
        score = (math.inf, -1)
        for j in range(len(clusters)):
            if i == j:
                continue
            currScore = getScore(clusters[i], clusters[j])
            if score[0] >= currScore[0]:
                score = currScore
        for j in range(len(clusters)):
            if i == j:
                continue
            currScore = getScore(clusters[i], clusters[j])
            if score[0] == currScore[0]:
                neighbours[map[y["name"]]].append((map[x["name"]], currScore[1]))
                neighbours[idMap[clusters[i]['name']]].append((idMap[clusters[j]['name']], currScore[1]))
        scoreClusterOrigin = getScore(clusters[i], origin)
        if score[0] >= scoreClusterOrigin[0]:
            neighbours[idMap[clusters[i]["name"]]].append((idMap[origin["name"]], scoreClusterOrigin[1]))  

# def bfs(ans, )
    
# def dfs(start, neighbours, idMap, gnomeMap, ans):
#     stack = collections.deque()
#     stack.append((start, ''))
#     while stack:
#         curr = stack.pop()

  

def dfs(start, ans, neighbours, idMap, gnomeMap, curr):
    if start != 0 and getScore(gnomeMap[start],gnomeMap[1])[0] == 0:
        ans.append(curr + " -> " + gnomeMap[start]["name"])
        return
    for neighbour in neighbours[start]:
        stupidSign = " -> " if start != 0 else ""  
        asterisk = '*' if neighbour[1] >= 2 else ""
        temp = curr
        curr += stupidSign + gnomeMap[start]['name'] + asterisk
        dfs(neighbour[0], ans, neighbours, idMap, gnomeMap, curr)
        curr = temp

def getScore(s1, s2):
    s1 = s1["genome"]
    s2 = s2["genome"]
    diff = 0
    firstDiff = 0
    for i in range(len(s1)):
        if(s1[i] != s2[i]):
            diff += 1
            if(i % 4 == 0):
                firstDiff += 1
    return (diff,firstDiff)
