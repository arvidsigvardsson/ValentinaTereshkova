#
# Basic RESTful API to Post and Get coordinates
#
from flask import Flask, jsonify, abort, make_response, request
from flask_restful import Api, reqparse
from api import CoordinateAPI, CoordinateListAPI, ObjectAPI, Resource

app = Flask(__name__)
api = Api(app)

coordinatelist = [
    {
        'x1' : 100,
        'y1' : 100,
        'x2' : 200,
        'y2' : 400
    },

    {
        'x1' : 200,
        'y1' : 200,
        'x2' : 200,
        'y2' : 400

    }
]

sockList = [
    {
        'x' : 500,
        'y' : 600
    }
]


#Handles 404 (not found) errors
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


class ObjectListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('object', type=str, required=True, location='json')
        self.reqparse.add_argument('x', type=str, required=True, location='json')
        self.reqparse.add_argument('y', type=str, required=True, location='json')
        super(ObjectListAPI, self).__init__()

    def get(self):
        return make_response(jsonify({'sock' : sockList}))

    def post(self):
        json_data = request.get_json(force=true)
        args = self.reqparse.parse_args()
        newObject = {
            'type' : args['type'],
            'x': args['x'],
            'y': args['y']
        }

class CoordinateListAPI(Resource):
    #Define arguments and how to validate them
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('x1', type=str, required=True, location='json')
        self.reqparse.add_argument('y1', type =str, required = True, location='json')
        self.reqparse.add_argument('x2', type=str, required=True, location='json')
        self.reqparse.add_argument('y2', type =str, required = True, location='json')
        super(CoordinateListAPI, self).__init__()

    def get(self):
        return make_response(jsonify({'coordinates': coordinatelist}))

    def post(self):
        json_data = request.get_json(force=True)
        args = self.reqparse.parse_args()
        coordinate = {
            'x1': args['x1'],
            'y1': args['y1'],
            'x2': args['x2'],
            'y2': args['y2']
        }
        coordinatelist.append(coordinate)
        return make_response(jsonify({'coordinate':(coordinate)}))

class CoordinateAPI(Resource):
    #Define arguments and how to validate them
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('x1', type = str, location='json')
        self.reqparse.add_argument('y1', type = str, location='json')
        self.reqparse.add_argument('x2', type = str, location='json')
        self.reqparse.add_argument('y2', type = str, location='json')
        super(CoordinateAPI,self).__init__()

    #Useless
    #Put for updating coordinates, not used right now
    def put(self):
        args = self.reqparse.parse_args()
        for k, v in args.iteritems():
            if v != None:
                coordinatelist[k] = v
        return make_response(jsonify( { 'coordinate': coordinate }))

    # Get- Returns the latest coordinate
    def get(self):
        coordinate = coordinatelist[-1]
        if coordinate == None:
            abort(404)
        return make_response(jsonify({ 'coordinate': coordinate }))


#add api:s
api.add_resource(ObjectListAPI, '/srv/objectlist', endpoint='objectlist')
api.add_resource(CoordinateListAPI, '/srv/coordinates', endpoint = 'coordinates')
api.add_resource(CoordinateAPI, '/srv/coordinate/getlatest', endpoint = 'coordinate')

if __name__ == '__main__':
    app.run(host ='0.0.0.0')
