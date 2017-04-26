#
# Basic RESTful API to Post and Get coordinates
#
from flask import Flask, jsonify, abort, make_response, request
from flask_restful import Api, reqparse
from api import CoordinateAPI, CoordinateListAPI, Resource
import json

app = Flask(__name__)
api = Api(app)

coordinatelist = [
    {
        'x' : 100,
        'y' : 100
    },

    {
        'x' : 200,
        'y' : 200

    }
]


#Handles 404 (not found) errors
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

class CoordinateListAPI(Resource):
    #Define arguments and how to validate them
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('x', type=str, required=True, location='json')
        self.reqparse.add_argument('y', type =str, required = True, location='json')
        super(CoordinateListAPI, self).__init__()

    def get(self):
        return make_response(json.dumps(coordinatelist))
        #return make_response(jsonify('coordinates' : coordinatelist))

    def post(self):
        json_data = request.get_json(force=True)
        args = self.reqparse.parse_args()
        coordinate = {
            'x': args['x'],
            'y': args['y']
        }
        coordinatelist.append(coordinate)
        return make_response(jsonify({'coordinate':(coordinate)}))

class CoordinateAPI(Resource):
    #Define arguments and how to validate them
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('x', type = str, location='json')
        self.reqparse.add_argument('y', type = str, location='json')
        super(CoordinateAPI,self).__init__()

    #Useless
    #Psut for updating coordinate, not used right now
    def put(self):
        args = self.reqparse.parse_args()
        for k, v in args.iteritems():
            if v != None:
                coordinatelist[k] = v
        return make_response(jsonify( { 'coordinate': coordinate}))

    # Get- Returns the latest coordinate
    def get(self):
        coordinate = coordinatelist[-1]
        if coordinate == None:
            abort(404)
        return make_response(jsonify({'coordinate': coordinate}))


#add api:s
api.add_resource(CoordinateListAPI, '/srv/coordinates', endpoint = 'coordinates')
api.add_resource(CoordinateAPI, '/srv/coordinate/getlatest', endpoint = 'coordinate')

if __name__ == '__main__':
    app.run(host ='0.0.0.0')
