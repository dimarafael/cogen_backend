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


class PostValue(Resource):
    def post(self, val_name):
        args = parser.parse_args()
        print(val_name, '=', args['value'])
        res = plc.set_smoke_fan_speed(int(args['value']))
        return {val_name: args['value'], 'result': res}


api.add_resource(GetData, '/api/data')
api.add_resource(PostValue, '/api/data/<string:val_name>')

plc = plc.Plc('localhost')
plc.start()

if __name__ == '__main__':
    app.run(debug=False)
