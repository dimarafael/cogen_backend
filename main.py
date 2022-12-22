from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
import plc

app = Flask(__name__)
api = Api(app)
CORS(app)


class GetData(Resource):
    def get(self):
        return plc.data


api.add_resource(GetData, '/data')


plc = plc.Plc('localhost')
plc.start()

if __name__ == '__main__':
    app.run(debug=False)
