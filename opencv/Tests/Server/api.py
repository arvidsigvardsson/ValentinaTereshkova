###
# Define methods for API:s, get / post for list and get / put / delete for single coordinate API
# Delete not used, might be in the future
###
from flask_restful import Resource


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

class ObjectAPI(Resource):
    def get(self):
        pass

    def post(self):
        pass
