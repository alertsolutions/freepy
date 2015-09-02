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

class AbstractIVRMenu(FiniteStateMachine, Switchlet):
  initial_state = 'not ready'

  transitions = [
    ('not ready', 'greeting'),
    ('greeting', 'routing'),
    ('routing', 'bridging'),
    ('bridging', 'routing'),
    ('routing', 'terminated'),
    ('routing', 'saying'),
    ('saying', 'routing'),
    ('routing', 'playing'),
    ('playing', 'routing'),
    ('routing', 'transfering'),
    ('transfering', 'routing')
  ]

  def __init__(self, *args, **kwargs):
    super(Monitor, self).__init__(*args, **kwargs)
    self.__logger__ = logging.getLogger('ivr.menu.AbstractIVRMenu')
    self.__dispatcher__ = None
    