from nose.tools import raises, with_setup

from rested_users.group_dao import GroupDAO
from rested_users.exceptions import UserError, GroupError


def initialize():
    groups = GroupDAO()
    group1 = {"name": "group1"}

    group2 = {"name": "group2"}

    return groups, group1, group2


def test_group_dao_create():

    groups, group1, group2 = initialize()

    result1 = groups.group_create(group1)
    result2 = groups.group_create(group2)

    assert group1 == result1
    assert group2 == result2

    groups = None


def test_group_dao_get():

    groups, group1, group2 = initialize()

    result1 = groups.group_create(group1)
    result2 = groups.group_create(group2)

    assert group1 == result1
    assert group2 == result2

    assert groups.group_get(group1['name']) == group1
    assert groups.group_get(group2['name']) == group2

    groups = None


@raises(GroupError)
def test_group_dao_delete():

    class MockGroupDAO(GroupDAO):
        def group_delete(self, name):
            group = self.group_get(name)
            del self.groups[name]

    groups = MockGroupDAO()

    result1 = groups.group_create({"name": "group1"})

    groups.group_delete("group1")
    groups.group_get("group1")

    groups = None


def test_group_dao_update():

    class MockGroupDAO(GroupDAO):
        def group_update(self, name, data):
            group = self.group_get(name)
            self.groups[name] = data
            return self.groups[name]


    groups = MockGroupDAO()

    result1 = groups.group_create({"name": "group1"})

    update1 = groups.group_update("group1", ["one", "two", "three"])

    assert update1 == ["one", "two", "three"]
    groups = None
