# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# Thomas Quintana <quintana.thomas@gmail.com>
from os import SEEK_END
from twisted.internet.protocol import Protocol, ReconnectingClientFactory

# Import the proper StringIO implementation.
try:
  from cStringIO import StringIO
except:
  from StringIO import StringIO

import logging
import urllib

class IEventSocketClientObserver(object):
  def on_event(self, event):
    pass

  def on_start(self, client):
    pass

  def on_stop(self):
    pass

class Event(object):
  def __init__(self, headers, body = None):
    self.__headers__ = headers
    self.__body__ = body

  def get_body(self):
    return self.__body__

  def get_header(self, name):
    return self.__headers__.get(name)

  def get_headers(self):
    return self.__headers__

class EventSocketClient(Protocol):
  def __init__(self, observer):
    self.__logger__ = logging.getLogger('freepy.lib.esl.eventsocketclient')
    # Data buffer.
    self.__buffer__ = None
    # Client state.
    self.__host__ = None
    self.__peer__ = None
    # Observer for incoming events.
    if isinstance(observer, IEventSocketClientObserver):
      self.__observer__ = observer
    else:
      raise TypeError('The observer must extend the \
      IEventSocketClientObserver interface.')

  def __parse__(self):
    # Make sure we have enough data to process the event.
    buffer_contents = self.__buffer__.getvalue()
    if len(buffer_contents) == 0 or not buffer_contents.find('\n\n'):
      return None
    else:
      # Parse the event for processing.
      self.__buffer__.seek(0)
      body = None
      headers = self.__parse_headers__()
      length = headers.get('Content-Length')
      if length:
        length = int(length)
        # Remove the Content-Length header.
        del headers['Content-Length']
        # Make sure we have enough data to process the body.
        offset = self.__buffer__.tell()
        self.__buffer__.seek(0, SEEK_END)
        end = self.__buffer__.tell()
        remaining = end - offset
        # Handle the event body.
        if length <= remaining:
          self.__buffer__.seek(offset)
          type = headers.get('Content-Type')
          if type and type == 'text/event-plain':
            headers.update(self.__parse_headers__())
            length = headers.get('Content-Length')
            if length:
              length = int(length)
              del headers['Content-Length']
              body = self.__buffer__.read(length)
          else:
            body = self.__buffer__.read(length)
        else:
          return None
      # Reclaim resources.
      offset = self.__buffer__.tell()
      self.__buffer__.seek(0, SEEK_END)
      end = self.__buffer__.tell()
      remaining = end - offset
      if remaining == 0:
        self.__buffer__.seek(0)
        self.__buffer__.truncate(0)
      else:
        self.__buffer__.seek(offset)
        data = self.__buffer__.read(remaining)
        self.__buffer__.seek(0)
        self.__buffer__.write(data)
        self.__buffer__.truncate(remaining)
      return Event(headers, body)

  def __parse_headers__(self):
    headers = dict()
    while True:
      line = self.__parse_line__()
      if line == '':
        break
      else:
        tokens = line.split(':', 1)
        name = tokens[0].strip()
        value = tokens[1].strip()
        if value and not len(value) == 0:
          value = urllib.unquote(value)
        headers.update({name: value})
    return headers

  def __parse_line__(self, stride = 64):
    line = list()
    while True:
      chunk = self.__buffer__.read(stride)
      end = chunk.find('\n')
      if end == -1:
        line.append(chunk)
      else:
        line.append(chunk[:end])
        offset = self.__buffer__.tell()
        left_over = len(chunk[end + 1:])
        self.__buffer__.seek(offset - left_over)
        break
      if len(chunk) < stride:
        break
    return ''.join(line)

  def connectionLost(self, reason):
    self.__logger__.critical('A connection to the FreeSWITCH instance located @ %s:%i \
    has been lost due to the following reason.\n%s', self.__peer__.host, 
    self.__peer__.port, reason)
    self.__observer__.on_stop()
    if self.__buffer__:
      self.__buffer__.close()
    self.__buffer__ = None
    self.__host__ = None
    self.__peer__ = None

  def connectionMade(self):
    self.__buffer__ = StringIO()
    self.__host__ = self.transport.getHost()
    self.__peer__ = self.transport.getPeer()
    self.__observer__.on_start(self)

  def dataReceived(self, data):
    if self.__logger__.isEnabledFor(logging.DEBUG):
      self.__logger__.debug('The following message was received from %s:%i.\n%s',
        self.__peer__.host, self.__peer__.port, data)
    self.__buffer__.write(data)
    while True:
      event = self.__parse__()
      if event:
        self.__observer__.on_event(event)
      else:
        break

  def send(self, command):
    serialized_command = str(command)
    if self.__logger__.isEnabledFor(logging.DEBUG):
      self.__logger__.debug('The following message will be sent to %s:%i.\n%s',
        self.__peer__.host, self.__peer__.port, serialized_command)
    self.transport.write(serialized_command)

class EventSocketClientFactory(ReconnectingClientFactory):
  def __init__(self, observer):
    self.__logger__ = logging.getLogger('freepy.lib.esl.eventsocketclientfactory')
    self.__observer__ = observer

  def buildProtocol(self, addr):
    if self.__logger__.isEnabledFor(logging.INFO):
      self.__logger__.info('Connected to the FreeSWITCH instance located @ %s:%i.',
        addr.host, addr.port)
    self.resetDelay()
    return EventSocketClient(self.__observer__)
