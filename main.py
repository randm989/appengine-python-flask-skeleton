"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask, render_template
from PythonChess.ChessBoard import ChessBoard
from PythonChess.ChessGUI_text import ChessGUI_text
from models.ChessUser import ChessUser

app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

from google.appengine.api import users


@app.route('/')
def hello():
	"""Return a friendly HTTP greeting."""
	user = users.get_current_user()
	if user:
		output = 'Hello %s!' % user.nickname()
		if users.is_current_user_admin():
			output += " You are an admin of this site"
		output += "\n%s\n%s\n%s\n" % (user.email(), user.user_id(), user.federated_provider())
		return output
	return "Hello World!"

@app.route('/signin')
def signin():
	user = users.get_current_user()
	if user:
		greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' % (user.nickname(), users.create_logout_url('/')))
	else:
		greeting = ('<a href="%s">Sign in or register</a>.' % users.create_login_url('/register'))

	return ('<html><body>%s</body></html>' % greeting)

@app.route('/register')
def register():
	user = users.get_current_user()
	if user:
		cu = ChessUser.get_by_id(user.user_id())
		if cu is None:
			cu = ChessUser(id = user.user_id(), userid = user.user_id(), username = user.nickname(), email=user.email())
			cu.put()
			return "New User Created for " + user.nickname()
		return "Welcome back, " + user.nickname()

	return "Please login before registering"

@app.route('/renderTest')
def renderTest():
	cb = ChessBoard(0)
	
	gui = ChessGUI_text()
	boardState = cb.GetState()
	gui.Draw(boardState)
	for i in xrange(len(boardState)):
		boardState[i] = ["." if x == "e" else x for x in boardState[i]]
	return render_template("chess_render.html", board = boardState)


@app.errorhandler(404)
def page_not_found(e):
	"""Return a custom 404 error."""
	return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def page_not_found(e):
	"""Return a custom 500 error."""
	return 'Sorry, unexpected error: {}'.format(e), 500
