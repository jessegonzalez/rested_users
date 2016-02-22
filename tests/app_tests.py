import rested_users.app

app = rested_users.app.app.test_client()


def test_invalid_namespace():
    rv = app.get('/foobar')
    assert rv.status_code == 404


def test_redirect():
    rv = app.get('/users')
    assert rv.status_code == 301


def test_missing_user():
    rv = app.get('/users/')
    assert rv.status_code == 405
    assert 'The method is not allowed for the requested URL.' in rv.data

    rv = app.get('/users/idonotexist')
    assert rv.status_code == 404


def test_user_create():
    user = {'first_name': 'Jesse',
            'last_name': 'Gonzalez',
            'userid': 'jesse'}
    rv = app.post('/users/', data=user)
    assert rv.status_code == 201

    rv = app.post('/users/', data=user)
    assert rv.status_code == 409


def test_user_get():
    rv = app.get('/users/jesse')
    print rv.status_code
    assert rv.status_code == 200


def test_user_update():
    user = {'first_name': 'Jesse',
            'last_name': 'Gonzalez Jr.',
            'userid': 'jesse'}

    rv = app.put('/users/jesse', data=user)
    assert rv.status_code == 200
    assert 'Gonzalez Jr.' in rv.data


def test_missing_group():
    rv = app.get('/groups/')
    assert rv.status_code == 405
    assert 'The method is not allowed for the requested URL.' in rv.data

    rv = app.get('/groups/idonotexist')
    assert rv.status_code == 404


def test_group_create():
    group = {'name': 'admin'}
    rv = app.post('/groups/', data=group)
    assert rv.status_code == 201

    rv = app.post('/groups/', data=group)
    assert rv.status_code == 409

    rv = app.get('/groups/admin')
    assert rv.status_code == 200


def test_group_update():
    members = {'members': ['jesse']}
    rv = app.put('/groups/admin', data=members)

    assert rv.status_code == 200

    rv = app.get('/users/jesse')
    assert rv.status_code == 200
    assert 'admin' in rv.data


def test_group_delete():
    rv = app.delete('/groups/admin')
    assert rv.status_code == 200

    rv = app.get('/groups/admin')
    assert rv.status_code == 404

    rv = app.get('/users/jesse')
    assert rv.status_code == 200
    assert 'admin' not in rv.data


def test_user_delete():
    rv = app.delete('/users/jesse')
    assert rv.status_code == 204

    rv = app.get('/users/jesse')
    assert rv.status_code == 404
