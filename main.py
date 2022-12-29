from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import plc
from tags import TAGS_BOOL, TAGS_NUMBER

app = Flask(__name__)
api = Api(app)
CORS(app)

parser = reqparse.RequestParser()
parser.add_argument('value')
parser.add_argument('tag')


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


def str_to_bool(s):
    if s == "True":
        return True
    elif s == "False":
        return False
    else:
        return None


class PostBool(Resource):
    def post(self):
        args = parser.parse_args()
        tag = args['tag']
        value = str_to_bool(args['value'])
        res = False
        if (tag in TAGS_BOOL.keys()) and value is not None:
            res = plc.set_bool(value, TAGS_BOOL[tag])
        return {tag: value, 'result': res}


class PostNumber(Resource):
    def post(self):
        args = parser.parse_args()
        tag = args['tag']
        value = args['value']
        res = False
        if (tag in TAGS_NUMBER.keys()) and value is not None:
            if type(value) == int or float:
                if TAGS_NUMBER[tag]['min'] <= float(value) <= TAGS_NUMBER[tag]['max']:
                    if TAGS_NUMBER[tag]['type'] == int:
                        res = plc.set_word(int(value), int(TAGS_NUMBER[tag]['address']))
                    elif TAGS_NUMBER[tag]['type'] == float:
                        res = plc.set_float(float(value), int(TAGS_NUMBER[tag]['address']))
        return {tag: value, 'result': res}


api.add_resource(GetData, '/api/data')
api.add_resource(PostSmokeFanSpeed, '/api/data/smoke_fan_speed')
api.add_resource(PostGazPreset, '/api/data/gaz_preset')
api.add_resource(PostBool, '/api/data/bool')
api.add_resource(PostNumber, '/api/data/number')

plc = plc.Plc('localhost')
plc.start()

if __name__ == '__main__':
    app.run(debug=False)
