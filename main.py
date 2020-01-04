from flask import Flask, request
from flask_restful import Resource, Api
from novelsList import fetchNovelsList

app = Flask(__name__)
api = Api(app)

class GetNovelsList(Resource):
    def get(self, page):
        return fetchNovelsList(page)

api.add_resource(GetNovelsList, '/novels/page/<int:page>')

if __name__ == '__main__':
    app.run(debug=True)