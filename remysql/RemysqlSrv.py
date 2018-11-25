"""

RemysqlSrv: remote command server. Run this on the PC with MySQL.

by:			zappfinger (Richard van Bemmelen)
version:	1.2
1.1		24-11-2018	: dump each record, convert datetime to string
1.2		25-11-2018	: added update option
"""

from pythonosc import dispatcher
from pythonosc import osc_server, udp_client
import threading, time, os
from queue import Queue
from DBclassMySQL import *
from os import listdir
from os.path import isfile, join
from subprocess import Popen, PIPE, STDOUT
import json

"""
	enter the ip address of the client machine to connect to
"""
##########################
otherIP = '192.168.1.121'
##########################

q = Queue()

class server():
	def __init__(self, ip, port):
		self.dispatcher = dispatcher.Dispatcher()
		self.dispatcher.map("/command", self.command_handler, "")
		self.dispatcher.map("/SQLcommand", self.SQLcommand_handler, "")

		self.server = osc_server.ThreadingOSCUDPServer((ip, port), self.dispatcher)

	def command_handler(self, unused_addr, args, cmdtext):
		print("{0}".format(cmdtext))
		if 'cd' in cmdtext:
			os.chdir(cmdtext.split()[1])
			res = os.getcwd()
		else:
			res=[]
			with Popen(cmdtext, stdout=PIPE, stderr=STDOUT, shell=True, universal_newlines=True) as process:
				for line in process.stdout:
					res.append(line)
		print(res)
		q.put(res)

	def SQLcommand_handler(self, unused_addr, args, qrytext):
		print("{0}".format(qrytext))
		res = ''
		try:
			if 'SELECT' in qrytext or 'select' in qrytext:
				res = db.select(qrytext)
			elif 'CREATE' in qrytext or 'create' in qrytext:
				res = db.exec(qrytext)
			elif 'INSERT' in qrytext or 'insert' in qrytext:
				res = db.exec(qrytext)
			elif 'UPDATE' in qrytext or 'update' in qrytext:
				res = db.exec(qrytext)
			elif 'DELETE' in qrytext or 'delete' in qrytext:
				res = db.exec(qrytext)
			if len(res)==0:
				res='OK'
		except MySQLError as e:
			print('Got error {!r}, errno is {}'.format(e, e.args[0]))
		print(res)
		q.put(res)



class client():
	def __init__(self, ip, port):
		self.client = udp_client.SimpleUDPClient(ip, port)

	def send(self):
		while 1:
			rep = q.get()
			for r in rep:
				self.client.send_message("/reply", json.dumps(r, indent=4, sort_keys=True, default=str))
				print(json.dumps(rep, indent=4, sort_keys=True, default=str))
			time.sleep(1)

if __name__ == "__main__":
	db = db()
	print('starting server')
	#
	def worker1():
		serv = server('0.0.0.0', 8889)
		print("Serving on {}".format(serv.server.server_address))
		serv.server.serve_forever()

	def worker2():
		clint = client(otherIP, 8889)
		clint.send()

	thread_list = []
	thread1 = threading.Thread(target=worker1)
	thread_list.append(thread1)
	thread1.start()
	thread2 = threading.Thread(target=worker2)
	thread_list.append(thread2)
	thread2.start()

while 1:
	time.sleep(.5)	# uses less CPU than pass
