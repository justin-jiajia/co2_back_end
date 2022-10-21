from apiflask import Schema
from apiflask.fields import String, List, Integer, Nested, DateTime


class TokenInSchema(Schema):
    username = String(required=True)
    password = String(required=True)


class TokenOutSchema(Schema):
    token = String()


class UserCreateInSchema(Schema):
    username = String(required=True)
    password = String(required=True)


class LogInSchema(Schema):
    value = Integer()
    o_type = String()
    co2_l = Integer()
    unit = String()


class LogOutSchema(Schema):
    id = Integer()
    value = Integer()
    o_type = String()
    co2_l = Integer()
    unit = String()
    timestamp = DateTime()


class LogsOut(Schema):
    logs = List(Nested(LogOutSchema))


class DayLogOut(Schema):
    id = Integer()
    value = Integer()
    timestamp = String()


class HomeOut(Schema):
    day_logs = List(Nested(DayLogOut))
    jf = Integer()
    jf_yesterday = Integer()
