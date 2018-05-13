# coding: utf-8
import logging
import os
import json

import jinja2
import webapp2
from webapp2_extras import sessions

from google.appengine.api import users

from common import util


def wsgi_app(routes):
    app = webapp2.WSGIApplication(routes, debug=True, config={
        'webapp2_extras.sessions': {
            'secret_key': 'k93ID9ZWrethBXam6d39'
        }
    })
    return app


# def user_required(handler):
#     def check_login(self, *args, **kwargs):
#         self.set_cookie('referer', self.request.path_qs)
#         if not self.session.get('user_id'):
#             self.redirect('/login')
#         else:
#             self.response.delete_cookie('referer')
#             return handler(self, *args, **kwargs)
#     return check_login


class BaseHandler(webapp2.RequestHandler):

    # @webapp2.cached_property
    # def user(self):
    #     from common.models import User
    #     user_id = self.session.get('user_id')
    #     if user_id:
    #         return User.get_by_id(long(user_id))
    #     return

    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()

    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)
        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)

    def get_jinja_env(self, file):
        jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader([
                os.path.dirname(file),
                "common/views",
            ]),
            extensions=['jinja2.ext.autoescape'],
            autoescape=True
        )
        return jinja_env

    def render_template(self, template, values):
        template_values = {
            'debug': util.debug,
            'app_id': util.app_id,
            'admin': users.is_current_user_admin()
        }
        template_values.update(values)
        html = template.render(template_values)
        self.response.write(html)

    def dashboard_page(self, user, template, values):
        if users.is_current_user_admin():
            self.render_template(template, values)
            return
        if not self.user:
            self.redirect('/login')
            return
        if self.user.key != user.key:
            self.message("error", "non hai accesso a questa pagina")
            self.redirect('/')
            return
        self.render_template(template, values)

    def json_response(self, _dict):
        logging.debug(_dict)
        self.response.headers['Content-Type'] = "application/json"
        self.response.write(json.dumps(_dict))

    def basic_auth_error(self):
        self.response.headers['WWW-Authenticate'] = 'Basic realm="Login!"'
        self.response.set_status(401)
        self.response.write('Login!')
        return

    def set_cookie(self, name, text):
        self.response.set_cookie(name, str(text), max_age=2592000)

    def del_cookie(self, name):
        self.response.delete_cookie(name)

    def get_cookie(self, name):
        return self.request.cookies.get(str(name))

    def message(self, color, text):
        _color = 'danger' if color == 'error' else color
        self.set_cookie('alert_color', _color)
        text = text.decode('utf-8').encode('ascii', 'ignore')
        self.set_cookie('alert_message', text)
        logging.debug(text)
