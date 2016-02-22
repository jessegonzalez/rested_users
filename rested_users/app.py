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
    'first_name': fields.String(required=False, description='The firstname of the user.', default=""),
    'last_name': fields.String(required=False, description='The lastname of the user.', default=""),
    'userid': fields.String(required=True, description='The userid of the user.'),
    'groups': fields.List(fields.String, required=False, description='A list of groups the user belongs to.',
                          default=[""])
})

group = api.model('group', {
    'name': fields.String(required=True, description='The name of the group.')
})

group_update = api.model('group_update', {
    'members': fields.List(fields.String, required=True, description='Updated membership list for the specified group.')
})

user_parser = api.parser()
user_parser.add_argument('first_name', type=str, required=False, help='The firstname of the user.')
user_parser.add_argument('last_name', required=False, help='The lastname of the user.')
user_parser.add_argument('userid', required=True, help='The userid of the user.')
user_parser.add_argument('groups', action='append', help='A list of groups the user belongs to.')

group_parser = api.parser()
group_parser.add_argument('name', type=str, required=True, help='The name of a group to add.')

group_update_parser = api.parser()
group_update_parser.add_argument('members', action='append', help='The list of users to add to this group.')


class DAO(GroupDAO, UserDAO):
    def __init__(self):
        super(DAO, self).__init__()

    def group_delete(self, groupname):
        try:
            self.group_get(groupname)
        except GroupError as e:
            api.abort(e.expr, e.msg)

        for _user in self.users:
            try:
                self.users[_user]['groups'].remove(groupname)
            except ValueError:
                pass

        del self.groups[groupname]
        return 204

    def group_update(self, name, data):
        print 'name:', name
        print 'data:', data

        for _user in data['members']:
            try:
                self.user_get(_user)
            except UserError:
                api.abort(409, 'One or more members provided is not valid.')

        for _user in data['members']:
            try:
                if name in self.users[_user]['groups']:
                    pass
            except TypeError:
                self.users[_user]['groups'] = [name]
            else:
                self.users[_user]['groups'].append(name)

        return data


dao = DAO()


@user_ns.route('/')
class UserCreate(Resource):
    @api.expect(user, validate=True)
    @api.response(201, 'Successful user creation')
    @api.response(409, 'Conflict with request data')
    def post(self):
        args = user_parser.parse_args()

        if args['groups'] is not None:
            for group in args['groups']:
                if group not in dao.groups:
                    api.abort(409, 'One or more provided groups is invalid.')
        try:
            return dao.user_create(args), 201
        except UserError as e:
            api.abort(e.expr, e.msg)


@user_ns.route('/<string:username>')
class UserWithID(Resource):
    @api.doc(params={'username': 'The username of the user to return.'})
    @api.response(200, 'Request successful')
    @api.response(404, 'Requested user not found')
    def get(self, username):
        try:
            return dao.user_get(username)
        except UserError as e:
            api.abort(e.expr, e.msg)

    @api.doc(params={'username': 'The username of the user to delete.'})
    @api.response(204, 'Requested user deletion successful')
    @api.response(404, 'Requested user not found')
    def delete(selfself, username):
        try:
            return dao.user_delete(username), 204
        except UserError as e:
            api.abort(e.expr, e.msg)

    @api.doc(params={'username': 'The username of the user to udpate.'})
    @api.expect(user, validate=True)
    @api.response(200, 'Update to user successful')
    @api.response(404, 'Requested user not found')
    def put(self, username):
        args = user_parser.parse_args()
        try:
            return dao.user_update(username, args)
        except UserError as e:
            api.abort(e.expr, e.msg)


@group_ns.route('/')
class GroupCreate(Resource):
    @api.expect(group)
    @api.response(201, 'Successful group creation')
    @api.response(409, 'Conflict with request data')
    def post(self):
        args = group_parser.parse_args()
        try:
            return dao.group_create(args), 201
        except GroupError as e:
            api.abort(e.expr, e.msg)


@group_ns.route('/<string:groupname>')
class GroupWithID(Resource):
    @api.doc(params={'groupname': 'The groupname of the list of users to return as a JSON list.'})
    @api.response(200, 'Request successful')
    @api.response(404, 'Requested group not found')
    def get(self, groupname):
        try:
            dao.group_get(groupname)
        except GroupError as e:
            api.abort(e.expr, e.msg)

        response = []
        for user in dao.users:
            try:
                user = dao.users[user]
                try:
                    for group in user["groups"]:
                        if group == groupname:
                            response.append(user['userid'])
                            break
                except TypeError:
                    pass
            except KeyError:
                pass
        return response

    @api.doc(params={'groupname': 'The groupname of the group to delete.'})
    @api.response(204, 'Requested group deletion successful')
    @api.response(404, 'Requested group not found')
    def delete(self, groupname):
        dao.group_delete(groupname)

    @api.doc(params={'groupname': 'The groupname to update the user membership.'})
    @api.expect(group_update)
    @api.response(200, 'Update to group successful')
    @api.response(404, 'Requested group not found')
    def put(self, groupname):
        args = group_update_parser.parse_args()
        dao.group_update(groupname, args)


if __name__ == '__main__':
    app.run(debug=True)
