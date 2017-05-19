# -*- coding: utf-8 -*-
from json import dumps

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from webob.exc import HTTPMethodNotAllowed

from blog.core import serialize
from models import Article, engine
from noodles.http import Response


session = Session(bind=engine)


def add_article(request):
    if not request.method != 'POST':
        raise HTTPMethodNotAllowed
    try:
        article = Article(user_id=request.params['user_id'],
                          title=request.params['title'],
                          text=request.params['text'])
        session.add(article)
        session.commit()
        response = dumps(serialize(article))
    except KeyError:
        response = 'query parameters was not provided'

    return Response(response)


def read(request, id):
    article = session.query(Article).filter(Article.id == id.path).one()
    json = dumps(serialize(article))
    return Response(json)


def list_articles(request):
    try:
        articles = session.query(Article).filter(
            Article.user_id == request.params['user_id']).all()
    except KeyError:
        articles = session.query(Article).all()
    json = dumps([serialize(article) for article in articles])
    return Response(json)


def delete_article(request, id):
    if not request.method != 'DELETE':
        raise HTTPMethodNotAllowed
    try:
        article = session.query(Article).filter(Article.id == id.path).one()
        session.delete(article)
        session.commit()
        message = 'article {} deleted'.format(article.title)
    except NoResultFound:
        message = 'article does not exist'

    return Response(message)
