#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates'),
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Blog(db.Model):
    title = db.StringProperty(required = True)
    essay = db.TextProperty(required = True)
    created = db.DateTimeProperty (auto_now_add = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):

    def render_front(self, title="", essay="", error=""):
        blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESc")
        self.render("front.html", title=title, essay=essay, error=error, blogs = blogs)


    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")
        essay   = self.request.get("essay")

        if title and essay:
            a = Blog(title= title, essay= essay)
            a.put()

            self.redirect("/")
        else:
            error = "we need both title and body text"
            self.render_front(title, essay, error)



app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
