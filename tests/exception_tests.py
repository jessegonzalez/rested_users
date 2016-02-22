from nose.tools import raises, with_setup

from rested_users.user_dao import UserDAO
from rested_users.group_dao import GroupDAO
from rested_users.exceptions import UserError, GroupError


@raises(UserError)
def test_user_dao_get_exception():
    users = UserDAO()
    users.user_get("unknown_user")


@raises(UserError)
def test_user_dao_delete_exception():
    users = UserDAO()
    users.user_delete("unknown_user")


@raises(UserError)
def test_user_dao_update_exception():
    users = UserDAO()
    users.user_update("unknown_user", {"foo": "bar"})


@raises(UserError)
def test_user_dao_create_exception_missing_userid():
    users = UserDAO()
    users.user_create({})


@raises(GroupError)
def test_group_dao_get_exception():
    groups = GroupDAO()
    groups.group_get("unknown_group")


@raises(NotImplementedError)
def test_group_dao_update_exception():
    groups = GroupDAO()
    groups.group_update("unknown_group", ["one", "two", "three"])


@raises(NotImplementedError)
def test_group_dao_delete_exception():
    groups = GroupDAO()
    groups.group_delete("unknown_group")


@raises(GroupError)
def test_group_dao_create_exception_missing_groupname():
    groups = GroupDAO()
    groups.group_create({})
