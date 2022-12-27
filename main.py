from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import plc

app = Flask(__name__)
api = Api(app)
CORS(app)

parser = reqparse.RequestParser()
parser.add_argument('value')

class GetData(Resource):
    def get(self):
        return plc.data


class PostSmokeFanSpeed(Resource):
    def post(self):
        args = parser.parse_args()
        res = plc.set_smoke_fan_speed(int(args['value']))
        return {'smoke_fan_speed': args['value'], 'result': res}


class PostGazPreset(Resource):
    def post(self):
        args = parser.parse_args()
        res = plc.set_gaz_preset(int(args['value']))
        return {'gaz_preset': args['value'], 'result': res}


api.add_resource(GetData, '/api/data')
api.add_resource(PostSmokeFanSpeed, '/api/data/smoke_fan_speed')
api.add_resource(PostGazPreset, '/api/data/gaz_preset')

plc = plc.Plc('localhost')
plc.start()

if __name__ == '__main__':
    app.run(debug=False)
