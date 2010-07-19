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
		return { 'queue_size': messages.qsize() }
		
	def put(self):
		log.debug('put called via %s: %s' % (request.method, request.GET))
		
		messages.put( { 'content': 'drill for great justice!', 'id': 1, 'number': '+64 21 712 171' } )
		messages.put( { 'content': 'Hey, what is doing down?', 'id': 2, 'number': '+64 21 712 171' } )
		messages.put( { 'content': 'Fire the main guns!!!', 'id': 3, 'number': '+64 21 712 171' } )
		messages.put( { 'content': 'Spray it, don\'t say it!', 'id': 4, 'number': '+64 21 712 171' } )

	@jsonify
	def get(self):
		try:
			msg = messages.get(block=False)
		except:
			return {}
		
		outgoing.put(msg)
	
		messages.task_done()	
		messages.save()
		
		return msg
