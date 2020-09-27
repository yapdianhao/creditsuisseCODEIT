import logging
import json

from collections import defaultdict

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/contact_trace', methods=['POST'])
def evaluateTrace():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    infected = data["infected"]
    origin = data["origin"]
    cluster = data["cluster"]
    answer = trace(infected, origin, cluster)

    return jsonify(answer);


def trace(infected, origin, cluster):

    adj = {}
    for i in range(2+len(cluster)):
        adj[i] = []
    map = dict()
    revmap = [None] * (len(cluster) + 10)
    map[infected["name"]] = 0
    revmap[0] = infected
    map[origin["name"]] = 1
    revmap[1] = origin
    id = 2
    for x in cluster:
        map[x["name"]] = id
        revmap[id] = x
        id += 1 

    min  = 1000
    for x in cluster:
        cmp = compare(x, infected)
        if min > cmp[0]:
            min = cmp[0]
    
    for x in cluster:
        print(map[infected["name"]], "<-->",map[x["name"]])
        cmp = compare(x, infected)
        if min == cmp[0]:
            adj[map[infected["name"]]].append((map[x["name"]], cmp[1]))
        

    print("min for ", map[infected["name"]], " is ", min)        

    print(map[infected["name"]], "<-->",map[origin["name"]])
    cmp = compare(origin, infected)
    if min >= cmp[0]:
        adj[map[infected["name"]]].append((map[origin["name"]], cmp[1]))


    for y in cluster:
        min = 1000
        for x in cluster:
            if y == x:
                continue
            cmp = compare(x, y)
            if min > cmp[0]:
                min = cmp[0]
        
        print("min for ", map[y["name"]], " is ", min)

        for x in cluster:
            print(map[y["name"]], "<-->",map[x["name"]])
            if y == x:
                continue
            cmp = compare(x, y)
            if min == cmp[0]:
                adj[map[y["name"]]].append((map[x["name"]], cmp[1]))
        
        print(map[y["name"]], "<-->",map[origin["name"]])
        cmp = compare(origin, y)
        if min >= cmp[0]:
            adj[map[y["name"]]].append((map[origin["name"]], cmp[1]))        

    print(adj)            

    answer = []
    findPath(0,"", answer, adj, map, revmap)
    return answer


def findPath(nextPerson, sequence, answer, adj, map, revmap):
    num = 0
    print("Next person:", nextPerson)
    print(adj)
    print(adj[nextPerson])
    if nextPerson != 0 and compare(revmap[nextPerson],revmap[1])[0] == 0:
        answer.append(sequence + " -> " + revmap[nextPerson]["name"])
        return
    for next in adj[nextPerson]:
        num += 1
        arrow = " -> "
        if nextPerson == 0:
            arrow = ""    

        if(next[1] >= 2):
            findPath(next[0], sequence + arrow + revmap[nextPerson]["name"] + "*" , answer, adj,  map, revmap)
        else:
            findPath(next[0], sequence + arrow + revmap[nextPerson]["name"] , answer, adj, map, revmap)   

def compare(a, b):
    sequence1 = a["genome"]
    sequence2 = b["genome"]
    numberOfDifferentCharacters = 0
    numberOfFirstCharacterChanges = 0
    for i in range(len(sequence1)):
        if(sequence1[i] != sequence2[i]):
            numberOfDifferentCharacters += 1
            if(i % 4 == 0):
                numberOfFirstCharacterChanges += 1
    # print(sequence1," ", sequence2,"=", numberOfDifferentCharacters)
    return (numberOfDifferentCharacters,numberOfFirstCharacterChanges)
