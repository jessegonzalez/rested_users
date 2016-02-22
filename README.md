rested_users - A simple user/group API.
=========================================================

Install
-------
Use pyenv, virtualenv, or virtualenv wrapper to create a virtualenv using python 2.7.x.

For example:
```
pyenv virtualenv 2.7.11 rested_users
pyenv activate rested_users
```

Clone this repository
---------------------
```
git clone https://github.com/jessegonzalez/rested_users.git
cd rested_users
```

Run Tests
---------
```
python setup.py test
```


Test Application in your Browser
----------------------
```
python setup.py install
python rested_users/app.py
```

Now navigate to http://localhost:5000 for some Swagger!
