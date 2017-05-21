# -*- coding: utf-8 -*-
from json import dumps

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from webob.exc import HTTPMethodNotAllowed

from core import serialize
from models import User, engine
from noodles.http import Response


session = Session(bind=engine)


def add_user(request):
    if not request.method != 'POST':
        raise HTTPMethodNotAllowed
    try:
        user = User(email=request.params['email'],
                    first_name=request.params['first_name'],
                    last_name=request.params['last_name'])
        session.add(user)
        session.commit()
        response = dumps(serialize(user))
    except KeyError:
        response = 'query parameters was not provided'

    return Response(response)


def detail_user(request, id):
    user = session.query(User).filter(User.id == id.path).one()
    json = dumps(serialize(user))

    return Response(json)


def list_users(request):
    users = session.query(User).all()
    json = dumps([serialize(user) for user in users])
    return Response(json)


def delete_user(request, id):
    if not request.method != 'DELETE':
        raise HTTPMethodNotAllowed
    try:
        user = session.query(User).filter(User.id == id.path).one()
        session.delete(user)
        session.commit()
        message = 'user {} deleted'.format(user.email)
    except NoResultFound:
        message = 'user does not exist'

    return Response(message)


def update_user(request, id):
    if not request.method != 'PATCH':
        raise HTTPMethodNotAllowed
    try:
        user = session.query(User).filter(User.id == id.path).one()
        user.email = request.params['email']
        user.first_name = request.params['first_name']
        user.last_name = request.params['last_name']
        session.commit()
        message = 'user {} updated'.format(user.email)
    except (NoResultFound, KeyError) as err:
        if isinstance(err, NoResultFound):
            message = 'user does not exist'
        else:
            message = 'please insert new values in query string'

    return Response(message)
