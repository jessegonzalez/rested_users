from rested_users.exceptions import UserError

class UserDAO(object):
    def __init__(self):
        self.users = {}
        super(UserDAO, self).__init__()

    def user_get(self, id):
        try:
            return self.users[id]
        except KeyError:
            raise UserError(404, "User with userid '{}' doesn't exist.".format(id))
    
    def user_create(self, data):

        try:
            userid = data['userid']
        except AttributeError:
            raise UserError(400, "Data missing 'userid' attribute.")
        except KeyError:
            raise UserError(400, "Data missing 'userid' attribute.")

        try:
            self.users[userid]
            raise UserError(409, "User with userid '{}' already exists.".format(userid))
        except KeyError:
            self.users[userid] = data
    
        return data

    def user_update(self, id, data):
        user = self.user_get(id)
        self.users[id] = data
        return self.users[id]

    def user_delete(self, id):
        user = self.user_get(id)
        del self.users[id]
