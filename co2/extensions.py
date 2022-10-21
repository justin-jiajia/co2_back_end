from apiflask import HTTPTokenAuth
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from authlib.jose import jwt, JoseError

db = SQLAlchemy()
auth = HTTPTokenAuth()
cors = CORS()

from .models import User


@auth.verify_token
def verify_token(token: str):
    try:
        data = jwt.decode(
            token.encode('ascii'),
            current_app.config['SECRET_KEY'],
        )
        id = data['id']
        user = User.query.get(id)
    except JoseError:
        return None
    except IndexError:
        return None
    return user
