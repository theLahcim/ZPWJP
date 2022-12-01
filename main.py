from utils import detection, argparser
import glob
from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

args = argparser()
files = glob.glob('images/*.jpg')
files.extend(glob.glob('images/*.png'))


class Dogs(Resource):
    @staticmethod
    def get():
        d = {}
        for f in files:
            d[f] = {}
            d[f] = detection(f, args["confidence"], 'dog')
        return d


class Cats(Resource):
    @staticmethod
    def get():
        d = {}
        for f in files:
            d[f] = {}
            d[f] = detection(f, args["confidence"], 'cat')
        return d


api.add_resource(Dogs, '/dogs')
api.add_resource(Cats, '/cats')

if __name__ == '__main__':
    app.run(debug=True)
