from google.appengine.ext import ndb

class ChessUser(ndb.Model):
	userid = ndb.StringProperty()
	username = ndb.StringProperty()
	email = ndb.StringProperty()
