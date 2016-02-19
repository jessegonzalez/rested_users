from rested_users.exceptions import GroupError

class GroupDAO(object):
    def __init__(self):
        self.groups = {}

    def group_get(self, name):
        try:
            return self.groups[name]
        except KeyError:
            raise GroupError(404, "Group with groupname '{}' doesn't exist.".format(name))

    def group_create(self, data):

        try:
            groupname = data['name']
        except AttributeError:
            raise GroupError(400, "Data missing 'name' attribute.")
        except KeyError:
            raise GroupError(400, "Data missing 'name' attribute.")

        try:
            self.groups[groupname]
            raise GroupError(409, "Group with groupname '{}' already exists.".format(groupname))
        except KeyError:
            self.groups[groupname] = data

        return self.groups[groupname]

    def group_update(self, name, data):
        raise NotImplementedError("GroupDAO.update must be overridden.")

    def group_delete(self, name):
        raise NotImplementedError("GroupDAO.delete must be overridden.")
