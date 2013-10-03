import webapp2
from google.appengine.ext import db
from google.appengine.api import users
from cgi import escape

class Greeting(db.Model):
    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.response.write('Hello %s' % user.nickname())
        else:
            self.response.write(
                'Hello World! [<a href=%s>sign in</a>]' % \
                users.create_login_url(self.request.uri)
            )   

        self.response.write('<h1>My GuestBook</h1><ol>')
        #greetings = db.GqlQuery("SELECT * FROM Greeting")
        greetings = Greeting.all()
        for greeting in greetings:
            self.response.write('<li> %s' % greeting.content)
        self.response.write('''
            </ol><hr>
            <form action="/sign" method=post>
            <textarea name=content rows=3 cols=60></textarea>
            <br><input type=submit value="Sign Guestbook">
            </form>
        ''')

class GuestBook(webapp2.RequestHandler):
    def post(self):
        greeting = Greeting()
        user = users.get_current_user()
        if user:
            greeting.author = user
        greeting.content = self.request.get('content')
        greeting.put()
        self.redirect('/')

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', GuestBook),
], debug=True)