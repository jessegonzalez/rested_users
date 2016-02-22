from nose.tools import raises, with_setup

from rested_users.user_dao import UserDAO
from rested_users.exceptions import UserError, GroupError


def initialize():
    users = UserDAO()
    user1 = {"first_name": "first1",
             "last_name": "last1",
             "userid": "id1",
             "groups": []}

    user2 = {"first_name": "first2",
             "last_name": "last2",
             "userid": "id2",
             "groups": []}

    return users, user1, user2


def test_user_dao_create():
    users, user1, user2 = initialize()

    result1 = users.user_create(user1)
    result2 = users.user_create(user2)

    assert user1 == result1
    assert user2 == result2

    users = None


def test_user_dao_get():
    users, user1, user2 = initialize()

    result1 = users.user_create(user1)
    result2 = users.user_create(user2)

    assert users.user_get(user1['userid']) == user1
    assert users.user_get(user2['userid']) == user2


@raises(UserError)
def test_user_dao_delete():
    users, user1, user2 = initialize()

    result1 = users.user_create(user1)
    result2 = users.user_create(user2)

    users.user_delete(user1['userid'])
    users.user_get(user1['userid'])

    users = None


def test_user_dao_update():
    users, user1, user2 = initialize()

    result1 = users.user_create(user1)
    result2 = users.user_create(user2)

    user1['first_name'] = "first_one"
    user2['first_name'] = "first_two"

    update1 = users.user_update(user1['userid'], user1)
    update2 = users.user_update(user2['userid'], user2)

    assert update1 == user1
    assert update2 == user2

    users = None
