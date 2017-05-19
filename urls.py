# -*- coding: utf-8 -*-
"""
filedesc: default url mapping
"""
from routes import Mapper
from config import DEBUG
from noodles.utils.maputils import urlmap
from routes.route import Route
import os


def get_map():
    " This function returns mapper object for dispatcher "
    map = Mapper()
    # Add routes here
    urlmap(map, [
        ('/', 'controllers#index'),
        #('/route/url', 'controllerName.actionName')
    ])

    # Old style map connecting
    #map.connect('Route_name', '/route/url', controller='controllerName',
    #action='actionName')

    if DEBUG:
        r = [Route(None, '/{path_info:.*}',
              controller='noodles.utils.static',
              action='index',
              path=os.path.join(os.getcwd(), 'static'),
              auth=True)]

        map.extend(r, '/static')

        user = [
                Route(None, '/create',
                      controller='noodles.blog.user_controller',
                      action='add_user'),
                Route(None, '/detail/:id',
                      controller='noodles.blog.user_controller',
                      action='detail_user'),
                Route(None, '/list',
                      controller='noodles.blog.user_controller',
                      action='list_users'),
                Route(None, '/delete/:id',
                      controller='noodles.blog.user_controller',
                      action='delete_user'),
                Route(None, '/update/:id',
                      controller='noodles.blog.user_controller',
                      action='update_user'),
                ]

        map.extend(user, '/user')

        article = [
                   Route(None, '/create',
                         controller='noodles.blog.article_controller',
                         action='add_article'),
                   Route(None, '/read/:id',
                         controller='noodles.blog.article_controller',
                         action='read'),
                   Route(None, '/list',
                         controller='noodles.blog.article_controller',
                         action='list_articles'),
                   Route(None, '/delete/:id',
                         controller='noodles.blog.article_controller',
                         action='delete_article'),
                   ]

        map.extend(article, '/article')

    return map
