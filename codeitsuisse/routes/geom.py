import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/revisitgeometry', methods=['POST'])
def evaluateGeom():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    shapeCoordinates = data['shapeCoordinates']
    lineCoordinates = data['lineCoordinates']
    ans = getIntersections(shapeCoordinates, lineCoordinates)
    logging.info("My result :{}".format(ans))
    return jsonify(ans);

def getIntersections(shapeCoordinates, lineCoordinates):
    line_x1 = lineCoordinates[0]['x']
    line_y1 = lineCoordinates[0]['y']
    line_x2 = lineCoordinates[1]['x']
    line_y2 = lineCoordinates[1]['y']
    ans = []
    if len(shapeCoordinates) == 1:
        shape_x1 = shapeCoordinates[0]['x']
        shape_y1 = shapeCoordinates[0]['y']
        if samePointSameLine(shape_x1, shape_y1, line_x1, line_y1, line_x2, line_y2):
            ans.append({'x': shape_x1, 'y': shape_y1})
    elif len(shapeCoordinates) == 2:
        shape_x1 = shapeCoordinates[0]['x']
        shape_y1 = shapeCoordinates[0]['y']
        shape_x2 = shapeCoordinates[1]['x']
        shape_y2 = shapeCoordinates[1]['y']
        if isParallel(shape_x1, shape_y1, shape_x2, shape_y2, line_x1, line_y1, line_x2, line_y2):
            return
        x, y = line_intersection(([line_x1, line_y1], [line_x2, line_y2]),
                                ([shape_x1, shape_y1], [shape_x2, shape_y2]))
        if ((shape_x1 - x) * (shape_x2 - x)) <= 0 and ((shape_y1 - y) * (shape_y2 - y)) <= 0:
            ans.append({'x': x, 'y': y})
    for i in range(len(shapeCoordinates)):
        j = (i + 1) % len(shapeCoordinates)
        shape_x1 = shapeCoordinates[i]['x']
        shape_y1 = shapeCoordinates[i]['y']
        shape_x2 = shapeCoordinates[j]['x']
        shape_y2 = shapeCoordinates[j]['y']
        if isParallel(shape_x1, shape_y1, shape_x2, shape_y2, line_x1, line_y1, line_x2, line_y2):
            return
        x, y = line_intersection(([line_x1, line_y1], [line_x2, line_y2]),
                                ([shape_x1, shape_y1], [shape_x2, shape_y2]))
        if ((shape_x1 - x) * (shape_x2 - x)) <= 0 and ((shape_y1 - y) * (shape_y2 - y)) <= 0:
            ans.append({'x': x, 'y': y})
    return ans

def isParallel(x1, y1, x2, y2, x3, y3, x4, y4):
    return (x2 - x1) * (y4 - y3) == (y2 - y1) * (x4 - x3)

def samePointSameLine(x1, y1, x2, y2, x3, y3):
    return (x3 - x2) * (y1 - y3) == (y3 - y2) * (x1 - y3)

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


