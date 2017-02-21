
import webapp2
import jinja2
import os

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates'),
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Post(db.Model):
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
    def get(self):
        self.redirect("/blog")


class BlogPage(Handler):
    def get(self):
        blogs = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 5")
        n = blogs.get()
        #b = n.key().id()
        self.render("posts.html", blogs = blogs)


class PostPage(Handler):
    def render_front(self, title="", essay="", error=""):
        self.render("create.html", title=title, essay=essay, error=error)

    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")
        essay   = self.request.get("essay")

        if title and essay:
            a = Post(title= title, essay= essay)
            a.put()
            n = a.key().id()

            self.redirect("/blog/" + str(n))
        else:
            error = "we need both title and body text"
            self.render_front(title, essay, error)

class ViewPostHandler(Handler):
    def get(self, id):
        post = Post.get_by_id(int(id))
        self.render("permalink.html", post = post)



app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/blog', BlogPage),
    ('/newpost', PostPage),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler),

], debug=True)
