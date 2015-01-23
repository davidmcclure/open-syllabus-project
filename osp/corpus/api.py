

from flask import Flask, Blueprint
import flask_restful


blueprint = Blueprint('corpus', __name__)
api = flask_restful.Api(blueprint)


class TextApi(flask_restful.Resource):

    def get(self):
        return {'osp': 'text'}


api.add_resource(TextApi, '/text')
