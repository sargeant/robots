import threading
import time
import logging
import shelve
import re
import subprocess
import random
import atexit

import feedparser

from pylons import config
from robots.lib.queue import messages, outgoing

log = logging.getLogger(__name__)

ShutdownMsg = object()

keyword = { 'fire': '1', 'drill': '2', 'spray': '3'}

class RobotControlThread(threading.Thread):
	start_command = ['sispmctl', '-o']
	stop_command = ['sispmctl', '-f']
	
	def shutdown(self):
		message.put(ShutdownMsg)
		
	def run(self):
		log.info("Robot control started")
		atexit.register(self.shutdown)
		
		while True:
			message = outgoing.get()
			if message == ShutdownMsg:
				log.debug("Shutdown")
				return
			if not keyword.has_key(message['keyword']):
				continue
				
			log.info("Launching %s robot" % message['keyword'])
			time.sleep(5)
			self._startRobot(keyword[message['keyword']])
			time.sleep(5)
			self._stopRobot(keyword[message['keyword']])

			outgoing.task_done()

	def _startRobot(self, i):
		args = self.start_command
		args.append(i)
		return self._runcmd(args)
	
	def _stopRobot(self, i):
		args = self.stop_command
		args.append(i)
		return self._runcmd(args)
		
	def _runcmd(self, args):
		log.debug("Launching command: %s" % args)
		try:
			return subprocess.call(args)
		except Exception, e:
			log.warn("Command failed: %s" % e)
			return		
			
class SonicPollerThread(threading.Thread):
	config = None
	first_word = re.compile('^\W*(\w+)\W*(.*)')
	
	def shutdown(self):
		print "shutdown, somehow"
		
	def run(self):
		log.info("Poller started")
		atexit.register(self.shutdown)
		
		
		while True:	
			history = shelve.open(self.config['poll.history'])

			feed = feedparser.parse(self.config['rss_feed'])
			feed.entries.reverse()
			for entry in feed.entries:
				if not history.has_key(str(entry.id)) and entry.description:
					log.debug("New message: %s" % entry.description)
					msg = { 'from': entry.title, 'date': entry.date }

					result = self.first_word.match(entry.description)
					if result:
						if result.group(1).lower() in keyword.keys():
							msg['keyword'] = result.group(1).lower()
							if result.group(2):
								msg['content'] = result.group(2)
							else:
								msg['content'] = result.group(1)
						else:
							msg['content'] = entry.description
							msg['keyword'] = random.choice(keyword.keys())
						
					log.debug("Adding to queue: %s" % msg)
					messages.put(msg)
					
				history[str(entry.id)] = True

			messages.save()
			history.close()
			log.debug("Finished poll. Queue size is %d" % messages.qsize())
			time.sleep(float(self.config['poll.interval']))
			
robotcontrol = RobotControlThread(name="robot control")	
poller = SonicPollerThread(name='poller')

