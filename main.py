from utils import detection, argparser
import glob
from flask import Flask
from flask_restful import Api, Resource
from flasgger import Swagger

app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'PetDetect',
    'uiversion': 3
}
api = Api(app)

swagger = Swagger(app)

args = argparser()
files = glob.glob('images/*.jpg')
files.extend(glob.glob('images/*.png'))


class Dogs(Resource):
    @staticmethod
    def get():
        """
               Use of class dogs
               Class checks if pictures in directory have dogs in them and if they do, how many of them
               To use call /dogs
               ---
               tags:
                - Pets
               parameters:
                 - in: path
               responses:
                 200:
                   description: dict of pictures of dogs
               """
        d = {}
        for f in files:
            d[f] = {}
            d[f] = detection(f, args["confidence"], 'dog')
        return d


class Cats(Resource):
    @staticmethod
    def get():
        """
         Use of class cats
         Class checks if pictures in directory have cats in them and if they do, how many of them
         To use call /cats
         ---
         tags:
            - Pets
         parameters:
           - in: path
         responses:
            200:
                description: dict of pictures of cats
       """
        d = {}
        for f in files:
            d[f] = {}
            d[f] = detection(f, args["confidence"], 'cat')
        return d


api.add_resource(Dogs, '/dogs')
api.add_resource(Cats, '/cats')

if __name__ == '__main__':
    app.run(host="0.0.0.0")


