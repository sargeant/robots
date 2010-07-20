import Queue
import cPickle as pickle
from pylons import config

class PersistentQueue(Queue.Queue):
	def save(self):
		if self.filename:
			pickle.dump(self.queue, open(self.filename, 'wb'))
		else:
			raise Exception
			
	def load(self, filename):
		self.filename = filename
		try:
			self.queue = pickle.load(open(filename, 'rb'))
		except IOError, err:
			if err.errno == 2: # not found
				pass
			else:
				raise err
				
messages = PersistentQueue()
outgoing = Queue.Queue()