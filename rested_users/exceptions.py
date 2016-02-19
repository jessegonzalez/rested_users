class Error(Exception):
    pass


class UserError(Error):
    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg


class GroupError(Error):
    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg
