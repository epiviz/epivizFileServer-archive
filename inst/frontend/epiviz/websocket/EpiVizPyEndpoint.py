'''
Created on Mar 12, 2014

@author: florin
'''

import math
import random

import simplejson
import tornado.websocket

from epiviz.events.EventListener import EventListener
from epiviz.websocket.Request import Request
from epiviz.websocket.Response import Response


class EpiVizPyEndpoint(tornado.websocket.WebSocketHandler):

    def __init__(self, *args, **kwargs):
        self._console_listener = kwargs.pop('console_listener')
        self._handler = kwargs.pop('handler')

        self._event_listener = EventListener(lambda command: self._handle_command(command))
        if not self._console_listener is None:

            self._console_listener.on_command_received().add_listener(self._event_listener)

        super(EpiVizPyEndpoint, self).__init__(*args, **kwargs)

    def check_origin(self, origin):
        return True

    def open(self):
        print 'new connection'

    def on_message(self, json_message):
        print 'message received %s' % json_message
#        message = simplejson.loads(json_message)
        self._handle_request(json_message)

    def on_close(self):
        if not self._console_listener is None:
            self._console_listener.on_command_received().remove_listener(self._event_listener.id())
        print 'connection closed'


    def send_request(self, request):
        '''
        :param request: Request
        '''

    def _handle_request(self, json_message):
        response = self._handler(json_message)
        print 'sending response %s' % response
        self.write_message(response)
