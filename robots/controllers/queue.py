import logging
import time
import re

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify

from robots.lib.base import BaseController, render
from robots.lib.queue import messages, outgoing

log = logging.getLogger(__name__)

class QueueController(BaseController):

	@jsonify
	def size(self):
		return { 'messages': messages.qsize(),
		 	'outgoing': outgoing.qsize() }
		
	def put(self):	
		messages.put( { 'keyword': request.GET['keyword'], 
				'content': request.GET['content'] } )
		return 'Message placed in queue: %s' % request.GET['content']

	@jsonify
	def get(self):
		try:
			msg = messages.get(block=False)
		except:
			return {}
		
		log.info("Displaying message: %s" % msg.get('content', ''))
		
		outgoing.put(msg)
		messages.save()		
		return msg
		
	def clear_messages(self):
		"""Remove all messages from the messages queue"""
		try:
			while True:
				messages.get(block=False)
		except:
			return 'Message queue empty'