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
# Cristian Groza  <frontc18@gmail.com>
#
# Thomas Quintana <quintana.thomas@gmail.com>

from freepy.lib.commands import *
from freepy.lib.core import *
from freepy.lib.fsm import *
from freepy.lib.server import Event, RegisterJobObserverCommand, UnregisterJobObserverCommand

import logging
import urllib

# Used ONLY by monitor to transition itself into the 'expecting heartbeat' state
# once it has had a chance to initialize.
class StartMonitorCommand(object):
  pass

class Monitor(FiniteStateMachine, Switchlet):
  initial_state = 'not ready'

  transitions = [
    ('not ready', 'ready'),
    ('ready', 'expecting heartbeat'),
    ('expecting heartbeat', 'expecting status response'),
    ('expecting status response', 'expecting status event'),
    ('expecting status event', 'processing status event'),
    ('processing status event', 'expecting heartbeat')
  ]

  def __init__(self, *args, **kwargs):
    super(Monitor, self).__init__(*args, **kwargs)
    self.__logger__ = logging.getLogger('heartbeat.monitor')
    self.__dispatcher__ = None

  @Action(state = 'ready')
  def initialize(self, message):
    self.__dispatcher__ = message.get_dispatcher()
    command = StartMonitorCommand()
    self.actor_ref.tell({'content': command})

  @Action(state = 'expecting status response')
  def handle_heartbeat(self, message):
    # Ask FreeSWITCH for a status.
    status_command = StatusCommand(self.actor_ref)
    # Always register to receive events for specific Job-UUIDs first.
    uuid = status_command.get_job_uuid()
    register_command = RegisterJobObserverCommand(self.actor_ref, uuid)
    self.__dispatcher__.tell({'content': register_command})
    self.__logger__.info('Registered to receive events with Job-UUID: %s' % uuid)
    # Send the status command.
    self.__dispatcher__.tell({'content': status_command})

  @Action(state = 'processing status event')
  def handle_status_event(self, message):
    self.__logger__.info(message.get_body())
    uuid = message.get_header('Job-UUID')
    command = UnregisterJobObserverCommand(uuid)
    self.__dispatcher__.tell({'content': command})
    self.__logger__.info('Unregistered to receive events with Job-UUID: %s' % uuid)
    command = StartMonitorCommand()
    self.actor_ref.tell({'content': command})

  def on_receive(self, message):
    # Necessary because all pykka messages must be dicts.
    message = message.get('content')
    if isinstance(message, InitializeSwitchletEvent):
      self.transition(to = 'ready', event = message)
    if isinstance(message, StartMonitorCommand):
      self.transition(to = 'expecting heartbeat')
    elif isinstance(message, Event):
      content_type = message.get_header('Content-Type')
      if content_type == 'command/reply':
        self.transition(to = 'expecting status event', event = message)
      elif content_type == 'text/event-plain':
        name = message.get_header('Event-Name')
        if name == 'HEARTBEAT':
          self.transition(to = 'expecting status response', event = message)
        elif name == 'BACKGROUND_JOB':
          self.transition(to = 'processing status event', event = message)
