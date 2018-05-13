# coding: utf-8
import logging
import json

from common.handlers import BaseHandler, wsgi_app


class HomeHandler(BaseHandler):

    def get(self):
        env = self.get_jinja_env(__file__)
        template = env.get_template('home.html')
        values = {}
        self.render_template(template, values)

APP = wsgi_app([
    ('/', HomeHandler),
])
