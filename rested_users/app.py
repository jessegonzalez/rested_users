from flask import Flask
from flask.ext.restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix

from rested_users import DESCRIPTION, TITLE, VERSION
from rested_users.group_dao import GroupDAO
from rested_users.user_dao import UserDAO
from rested_users.exceptions import GroupError, UserError


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version=VERSION, title=TITLE,
    description=DESCRIPTION,
)

group_ns = api.namespace('groups', description='Group operations')
user_ns = api.namespace('users', description='User operations')

user = api.model('user', {
    'first_name': fields.String(required=False, description='The firstname of the user.'),
    'last_name': fields.String(required=False, description='The lastname of the user.'),
    'userid': fields.String(required=True, description='The userid of the user.'),
    'groups': fields.List(fields.String, required=False, description='A list of groups the user belongs to.')
})

class DAO(UserDAO, GroupDAO):
    def delete_group(self):
        pass

    def update_group(self):
        pass


dao = DAO()

@user_ns.route('/')
class UserCreate(Resource):
    @api.expect(user)
    def post(self):
        try:
            return dao.user_create(api.payload)
        except UserError as e:
            api.abort(e.expr, e.msg)


@user_ns.route('/<string:username>')
class UserWithID(Resource):
    @api.doc(params={'username': 'The username of the user to return.'})
    def get(self, username):
        try:
            return dao.user_get(username)
        except UserError as e:
            api.abort(e.expr, e.msg)

    @api.doc(params={'username': 'The username of the user to delete.'})
    def delete(selfself, username):
        try:
            return dao.user_delete(username)
        except UserError as e:
            api.abort(e.expr, e.msg)

    @api.doc(params={'username': 'The username of the user to udpate.'})
    @api.expect(user)
    def put(self, username):
        try:
            return dao.user_update(username, api.payload)
        except UserError as e:
            api.abort(e.expr, e.msg)

if __name__ == '__main__':
    app.run(debug=True)