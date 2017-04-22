#
# Basic RESTful API to Post and Get coordinates
#
from flask import Flask, jsonify, abort, make_response, request
from flask_restful import Api, Resource, reqparse

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

class CoordinateListAPI(Resource):
    def get(self):
        pass

    def post(self):
        pass

class CoordinateAPI(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

class CoordinateListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('x', type=str, required=True, location='json')
        self.reqparse.add_argument('y', type =str, required = True, location='json')
        super(CoordinateListAPI, self).__init__()

    def get(self):
        return make_response(jsonify({'coordinates': coordinatelist}))

    def post(self):
        args = self.reqparse.parse_args()
        coordinate = {
            'x': args['x'],
            'y': args['y'],
        }
        coordinatelist.append(coordinate)
        return make_response(jsonify({'coordinate':(coordinate)}))

class CoordinateAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('x', type = str, location='json')
        self.reqparse.add_argument('y', type = str, location='json')
        super(CoordinateAPI,self).__init__()


    #Useless
    def put(self):
        args = self.reqparse.parse_args()
        for k, v in args.iteritems():
            if v != None:
                coordinatelist[k] = v
        return make_response(jsonify( { 'coordinate': coordinate}))

    def get(self):
        coordinate = coordinatelist[-1]
        if coordinate == None:
            abort(404)
        return make_response(jsonify({'coordinate': coordinate}))


api.add_resource(CoordinateListAPI, '/todo/api/v1.0/coordinates', endpoint = 'coordinates')
api.add_resource(CoordinateAPI, '/todo/api/v1.0/coordinate/getlatest', endpoint = 'coordinate')

if __name__ == '__main__':
    app.run(host ='0.0.0.0')
