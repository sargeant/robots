import threading
import time
import logging
import ftplib
import shelve
import re

from pylons import config
from robots.lib.queue import messages, outgoing

log = logging.getLogger(__name__)

class RobotControlThread(threading.Thread):
	first_word_regexp = re.compile('^\W*(\w+)')
	action_index = { 'fire': 1, 'drill': 2, 'spray': 3}
	start_action = 'sispmctl -o %d'
	stop_action = 'sispmctl -f %d'
	
	def run(self):
		log.info("Robot control started")

		while True:
			message = outgoing.get()
			result = self.first_word_regexp.match(message['content'])
			if result.group(1):
				word = result.group(1).lower()
				if self.action_index.has_key(word):
					log.info("Launching %s robot" % word)
					time.sleep(5)
					self._runcmd(self.start_action % self.action_index[word])
					time.sleep(5)
					self._runcmd(self.stop_action % self.action_index[word])
			outgoing.task_done()

	def _runcmd(self, command):
		log.debug("cmd: %s" % command)
			
class SonicPollerThread(threading.Thread):
	config = None
	
	def run(self):
		log.info("Poller started")
		
		while True:	
			file_history = shelve.open(self.config['poll.history'])
			log.debug("Connnecting to %s" % self.config['poll.host'])
			try:
				ftp = ftplib.FTP(
					host=self.config['poll.host'], 
					user=self.config['poll.username'],
					passwd=self.config['poll.password'])
				ftp.login()
				ftp.set_pasv(self.config['poll.passive_mode'])
				ftp.cwd(self.config['poll.remote_dir'])
				for file in ftp.nlst(): # TODO: Order by timestamp/filename
					if not file_history.has_key(file):
						log.debug('processing: %s' % file)
						ftp.retrlines('RETR %s' % file, self.process_line)
						file_history[file] = True					
				ftp.quit()
			except ftplib.all_errors, err:
				log.warning("FTP Exception: %s", err)
				
			file_history.close()
			log.debug("Finished poll. Queue size is %d" % messages.qsize())
			time.sleep(float(self.config['poll.interval']))
			
	def process_line(self, line):
		messages.put( {'content': line } )
		messages.save()

robotcontrol = RobotControlThread(name="robot control")	
poller = SonicPollerThread(name='poller')

