class HealthStatus(object):

    def __init__(self, name: str, http_code: int):
        self.name = name
        self.http_code = http_code

    @classmethod
    def PASS(cls):
        return cls('pass', 200)

    @classmethod
    def FAIL(cls):
        return cls('fail', 500)

    @classmethod
    def WARN(cls):
        return cls('warn', 300)
