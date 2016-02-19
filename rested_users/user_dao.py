from rested_users.exceptions import UserError

class UserDAO(object):
    def __init__(self):
        self.users = {}

    def get(self, id):
        try:
            return self.users[id]
        except KeyError:
            raise UserError(404, "User with userid '{}' doesn't exist.".format(id))
    
    def create(self, data):

        try:
            userid = data['userid']
        except AttributeError:
            raise UserError(400, "Data missing 'userid' attribute.")

        try:
            self.users[userid]
            raise UserError(409, "user with userid '{}' already exists.".format(userid))
        except KeyError:
            self.users[userid] = data
    
        return data

    def update(self, id, data):
        user = self.get(id)
        self.users[id] = data
        return self.users[id]

    def delete(self, id):
        user = self.get(id)
        del self.users[id]
