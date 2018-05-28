# coding: utf-8
import logging
import json

from common.handlers import BaseHandler, wsgi_app

from common.google_api import call_vision_api


class HomeHandler(BaseHandler):

    def get(self):
        env = self.get_jinja_env(__file__)
        template = env.get_template('home.html')
        values = {
            'result': ''
        }
        self.render_template(template, values)

    # def post(self):
    #     result = call_vision_api()
    #     env = self.get_jinja_env(__file__)
    #     template = env.get_template('home.html')
    #     values = {
    #         'result': result
    #     }
    #     self.render_template(template, values)



APP = wsgi_app([
    ('/', HomeHandler),
])
