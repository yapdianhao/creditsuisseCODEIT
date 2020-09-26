import logging
import json
import collections

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/intelligent-farming', methods=['POST'])
def evaluateGMO():
    data = request.get_json();
    #logging.info("data sent for evaluation {}".format(data))
    for i in range(len(data['list'])):
        data['list'][i]['geneSequence'] = crop(data['list'][i]['geneSequence'])
        #logging.info("score for " + str(i) + " : " + str(data['list'][i]['geneSequence'].count('ACGT')  * 15 + data['list'][i]['geneSequence'].count('CC') * 25 - data['list'][i]['geneSequence'].count('AAA') * 10))
    #logging.info(data)
    return jsonify(data);

def crop(sequence):
    d = collections.Counter(sequence)
    newSeq = ''
    if (d['C'] // 2) * 25 > min(d['A'], d['C'], d['G'], d['T']) * 15:
        newSeq = ''
        newSeq += 'CC' * (d['C'] // 2)
        d['C'] %= 2
        acgt = min(d['A'], d['C'], d['G'], d['T'])
        newSeq += 'ACGT' * acgt
        d['A'] -= acgt
        d['C'] -= acgt
        d['G'] -= acgt
        d['T'] -= acgt
        noA = ''
        for i in d:
            if i != 'A':
                noA += i * d[i]
        remaining = ''
        counter = min(len(noA), d['A'] // 2)
        for i in range(counter):
            remaining += 'AA'
            remaining += noA[0]
            noA = noA[1:]
        newSeq += remaining
        if noA:
            newSeq += noA
        else:
            newSeq += 'A' * (d['A'] - counter * 2)
    else:
        acgt = min(d['A'], d['C'], d['G'], d['T'])
        newSeq += 'ACGT' * acgt
        d['A'] -= acgt
        d['C'] -= acgt
        d['G'] -= acgt
        d['T'] -= acgt
        newSeq += 'CC' * (d['C'] // 2)
        d['C'] %= 2
        noA = ''
        for i in d:
            if i != 'A':
                noA += i * d[i]
        remaining = ''
        counter = min(len(noA), d['A'] // 2)
        for i in range(counter):
            remaining += 'AA'
            remaining += noA[0]
            noA = noA[1:]
        newSeq += remaining
        if noA:
            newSeq += noA
        else:
            newSeq += 'A' * (d['A'] - counter * 2)
    if len(sequence) != len(newSeq):
        logging.info(sequence)
    return newSeq
