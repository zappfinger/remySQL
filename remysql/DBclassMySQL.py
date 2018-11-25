#
#   DBclass for MySQL
#	15-09-2018:	made it 3.5 compatible
#	24-11-2018:	added catch for select
#
import pymysql.cursors
from pymysql.err import ProgrammingError

showinserts = 0
showupdates = 0
showselects = 1
showupdates = 0
showexec = 0


class db(object):
	def __init__( self, dbname='robot'):
		self.conn = pymysql.connect(cursorclass=pymysql.cursors.DictCursor,
			host="127.0.0.1",
			user="xxxx",
			passwd="xxxx",
			database=dbname,

		)
		self.cur=self.conn.cursor()
		print(self.conn)

	def insert(self, insq, tup):
		if showinserts: print(insq, tup)
		try:
			self.cur.execute(insq, tup)
			self.conn.commit()
			#print self.cur.rowcount
		except ProgrammingError as e:
			print(e)
			print("Error {}: {}".format(e.args[0], e.args[1]))

	def update(self, upq):
		if showupdates:print(upq)
		try:
			self.cur.execute(upq)
			self.conn.commit()
			#print self.cur.rowcount
		except ProgrammingError as e:
			print("Error %s:" % e.args[0])

	def exec(self, exq):
		if showexec:print(exq)
		try:
			self.cur.execute(exq)
			self.conn.commit()
			#print self.cur.rowcount
		except ProgrammingError as e:
			print("Error %s:" % e.args[0])


	def select(self, selq):
		if showselects: print(selq)
		try:
			self.cur.execute(selq)
			rows = self.cur.fetchall()
			return rows
		except ProgrammingError as e:
			return "Error %s:" % e.args[0]

	def exists(self, selq):     # returns true or false depending on query
		self.cur.execute(selq)
		rows = self.cur.fetchall()
		if len(rows) == 0:
			result = False
		else:
			result = True
		return result


if __name__ == '__main__':
	mydb = db()
	result = mydb.select("select * from todo")
	print(result)
