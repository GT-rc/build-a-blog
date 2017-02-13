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
import os
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    # def render_front(self, title="", blog="", error=""):
    #
    #     self.render('base.html', title=title, blog=blog, error=error, blogs=blogs)

class Blog(db.Model):
    title = db.StringProperty(required=True)
    body = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

class MainHandler(Handler):
    def get(self):
        blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC LIMIT 5")
        self.render("home.html")
        # t = jinja_env.get_template("home.html")
        # content = t.render(blogs=blogs)
        # self.render(content)

class NewPostHandler(Handler):
    def get(self):

        t = jinja_env.get_template("newpost.html")
        content = t.render()
        self.response.write(content)

    def post(self, id):
        title = self.request.get("title")
        blog = self.request.get("blog")

        # Text is already escaped by the template, so no need to do that here.

        if not title and body:
            error = "Please enter both a title and a blog post."
            self.render('newpost.html', title, blog, error)
        else:
            ipsum = Blog(title=title, blog=blog)
            ipsum.put()

            self.redirect('/blog/{}'.format(id))

class PermalinkHandler(Handler):
    pass


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/blogs', NewPostHandler),
    webapp2.Route('/blog/<id:\d+>', PermalinkHandler)
], debug=True)
