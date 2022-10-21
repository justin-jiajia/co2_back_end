from co2.models import User, Log, DayLog
from co2.extensions import db, auth
from co2.api.v1 import api_v1
from co2.api.v1.schemas import *
from co2.functions import now_time
from apiflask import abort


@api_v1.post('/user/')
@api_v1.input(UserCreateInSchema)
@api_v1.output(TokenOutSchema)
def create_user(data):
    if User.query.filter_by(username=data['username']).first():
        abort(400, f'用户名为{data["username"]}的用户已存在')
    user = User()
    user.username = data['username']
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    token = user.get_token()
    return {
        'token': f'Bearer {token}'
    }


@api_v1.post('/oath/token/')
@api_v1.input(TokenInSchema)
@api_v1.output(TokenOutSchema)
def get_token(data):
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        abort(404, '用户名或密码错误')
    if not user.validate_password(data['password']):
        abort(404, '用户名或密码错误')
    return {
        'token': f'Bearer {user.get_token()}'
    }


@api_v1.get('/home/')
@api_v1.output(HomeOut)
@auth.login_required()
def get_home_data():
    return auth.current_user


@api_v1.post('/log/')
@api_v1.input(LogInSchema)
@api_v1.output(HomeOut)
@auth.login_required()
def create_log(data):
    item = Log()
    item.value = data['value']
    item.o_type = data['o_type']
    item.co2_l = data['co2_l']
    item.unit = data['unit']
    item.author = auth.current_user
    db.session.add(item)
    cc = False
    nw = DayLog.query.filter(DayLog.author == auth.current_user) \
        .filter(DayLog.timestamp == now_time()).one_or_none()

    if nw is None:
        cc = True
        nw = DayLog()
        nw.timestamp = now_time()
        nw.author = auth.current_user
        nw.value = 0
    nw.value += data['co2_l']
    if cc:
        db.session.add(nw)
    db.session.commit()
    return auth.current_user


@api_v1.get('/log/')
@api_v1.output(LogsOut)
@auth.login_required()
def get_logs():
    return auth.current_user
