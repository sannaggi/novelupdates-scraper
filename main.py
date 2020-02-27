from flask import Flask, request
from flask_restful import Resource, Api
from novels.novels import fetchNovelsList
from novels.novel import fetchNovel

app = Flask(__name__)
api = Api(app)

class GetNovelsList(Resource):
    def get(self):
        sort = request.args['sort']
        order = request.args['order']
        status = request.args['status']
        page = request.args['page']

        return fetchNovelsList(sort, order, status, page)

class GetNovel(Resource):
    def get(self, name):
        return fetchNovel(name)

api.add_resource(GetNovelsList, '/novels')
api.add_resource(GetNovel, '/novels/<string:name>')

if __name__ == '__main__':
    app.run(debug=True)