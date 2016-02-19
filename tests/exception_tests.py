from nose.tools import raises, with_setup

from rested_users.user_dao import UserDAO
from rested_users.exceptions import UserError, GroupError


@raises(UserError)
def test_user_dao_get_exception():
    users = UserDAO()
    users.get("unknown_user")


@raises(UserError)
def test_user_dao_delete_exception():
    users = UserDAO()
    users.delete("unknown_user")


@raises(UserError)
def test_user_dao_update_exception():
    users = UserDAO()
    users.update("unknown_user", {"foo": "bar"})

