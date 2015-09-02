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

from llist import dllist
from pykka import ThreadingActor
from threading import Thread

import logging, time

class ServiceRequest(object):
  pass

class ReceiveTimeoutCommand(ServiceRequest):
  def __init__(self, sender, timeout, recurring = False):
    self.__sender__ = sender
    self.__timeout__ = timeout
    self.__recurring__ = recurring

  def get_sender(self):
    return self.__sender__

  def get_timeout(self):
    return self.__timeout__

  def is_recurring(self):
    return self.__recurring__

class StopTimeoutCommand(ServiceRequest):
  def __init__(self, sender):
    self.__sender__ = sender

  def get_sender(self):
    return self.__sender__

class ClockEvent(object):
  pass

class TimeoutEvent(object):
  pass

class MonotonicClock(Thread):
  def __init__(self, *args, **kwargs):
    super(MonotonicClock, self).__init__(group = None)
    self.__actor__ = args[0]
    self.__interval__ = args[1]
    self.__running__ = True
    # Singleton instance of ClockEvent.
    self.__event__ = ClockEvent()

  def run(self):
    while self.__running__:
      time.sleep(self.__interval__)
      if self.__running__:
        self.__actor__.tell({'content': self.__event__})
      else:
        break

  def stop(self):
    self.__running__ = False

class TimerService(ThreadingActor):
  '''
  The timer service uses the timing wheel algorithm borrowing from the
  approach used in the Linux kernel. Please refer to the email thread
  by Ingo Molnar @ https://lkml.org/lkml/2005/10/19/46.
  '''
  TICK_SIZE  = 0.1             # Tick every 100 milliseconds.

  def __init__(self, *args, **kwargs):
    super(TimerService, self).__init__(*args, **kwargs)
    # Initialize the timing wheels. The finest possible
    self.__logger__ = logging.getLogger('freepy.lib.services.TimerService')
    # granularity is 100ms.
    self.__timer_vector1__ = self.__create_vector__(256)
    self.__timer_vector2__ = self.__create_vector__(256)
    self.__timer_vector3__ = self.__create_vector__(256)
    self.__timer_vector4__ = self.__create_vector__(256)
    # Initialize the timer vector indices.
    self.__timer_vector2_index__  = 0
    self.__timer_vector3_index__  = 0
    self.__timer_vector4_index__  = 0
    # Initialize the tick counter.
    self.__current_tick__ = 0
    # Initialize the actor lookup table for O(1) timer removal.
    self.__actor_lookup_table__ = dict()
    # Singleton instance of the timeout event.
    self.__timeout__ = TimeoutEvent()
    # Monotonic clock.
    self.__clock__ = None

  def __cascade_vector__(self, vector, elapsed):
    '''
    Cascades all the timers inside a vector to a lower bucket.

    Arguments: vector  - The vector to cascade.
               elapsed - The amount of time elapsed in milliseconds.
    '''
    for index in range(1, len(vector)):
      bucket = vector[index]
      previous_bucket = vector[index - 1]
      while len(bucket) > 0:
        timer = bucket.popleft()
        expires = timer.get_expires() - elapsed
        timer.set_expires(expires)
        node = previous_bucket.append(timer)
        self.__update_lookup_table__(previous_bucket, node)

  def __cascade_vector_2__(self):
    '''
    Cascades timers from vector 2 into vector 1.
    '''
    tick = self.__current_tick__
    timers = self.__timer_vector2__[0]
    for timer in timers:
      expires = timer.get_expires() - 25600
      timer.set_expires(expires)
      self.__vector1_insert__(timer)
    timers.clear()
    self.__cascade_vector__(self.__timer_vector2__, 25600)
    index = self.__timer_vector2_index__
    index = (index + 1) % 256
    self.__timer_vector2_index__ = index
    if self.__timer_vector2_index__ == 0:
      self.__cascade_vector_3__()

  def __cascade_vector_3__(self):
    '''
    Cascades timers from vector 3 into vector 2.
    '''
    tick = self.__current_tick__
    timers = self.__timer_vector3__[0]
    for timer in timers:
      expires = timer.get_expires() - 6553600
      timer.set_expires(expires)
      self.__vector2_insert__(timer)
    timers.clear()
    self.__cascade_vector__(self.__timer_vector3__, 6553600)
    index = self.__timer_vector3_index__
    index = (index + 1) % 256
    self.__timer_vector3_index__ = index
    if self.__timer_vector3_index__ == 0:
      self.__cascade_vector_4__()

  def __cascade_vector_4__(self):
    '''
    Cascades timers from vector 4 into vector 3.
    '''
    tick = self.__current_tick__
    timers = self.__timer_vector4__[0]
    for timer in timers:
      expires = timer.get_expires() - 1677721600
      timer.set_expires(expires)
      self.__vector3_insert__(timer)
    timers.clear()
    self.__cascade_vector__(self.__timer_vector4__, 1677721600)
    index = self.__timer_vector4_index__
    index = (index + 1) % 256
    self.__timer_vector4_index__ = index

  def __create_vector__(self, size):
    '''
    Creates a new vector and initializes it to a specified size.

    Arguments: size - The size of the vector.
    '''
    vector = list()
    for counter in range(size):
      vector.append(dllist())
    return vector

  def __round__(self, timeout):
    '''
    Rounds a timeout to the nearest multiple of the tick size.

    Arguments: timeout - The timeout to be rounded.
    '''
    if timeout < 100:
      return 100
    remainder = timeout % 100
    if remainder == 0:
      return timeout
    elif remainder <= 49:
      return  timeout - remainder
    else:
      return timeout + 100 - remainder

  def __schedule__(self, timer):
    '''
    Schedules a timer for expiration.

    Arguments: timer - The timer to be shceduled.
    '''
    tick = self.__current_tick__
    timeout = timer.get_timeout()
    expires = (tick % 256) * 100 + self.__round__(timeout)
    timer.set_expires(expires)
    if expires <= 25600:
      self.__vector1_insert__(timer)
    elif expires <= 6553600:
      self.__vector2_insert__(timer)
    elif expires <= 1677721600:
      self.__vector3_insert__(timer)
    elif expires <= 429496729600:
      self.__vector4_insert__(timer)

  def __tick__(self):
    '''
    Excutes one clock tick.
    '''
    tick = self.__current_tick__
    timers = self.__timer_vector1__[tick % 256]
    recurring = list()
    while len(timers) > 0:
      timer = timers.popleft()
      timer.get_observer().tell({'content': self.__timeout__})
      if timer.is_recurring():
        recurring.append(timer)
      else:
        lookup_table = self.__actor_lookup_table__
        urn = timer.get_observer().actor_urn
        location = lookup_table.get(urn)
        if location:
          del lookup_table[urn]
    for timer in recurring:
      self.__schedule__(timer)
    self.__current_tick__ = tick + 1
    if self.__current_tick__ % 256 == 0:
      self.__cascade_vector_2__()

  def __unschedule__(self, command):
    '''
    Unschedules a timer that has previously been scheduled for expiration.

    Arguments: command - The StopTimeoutCommand.
    '''
    urn = command.get_sender().actor_urn
    location = self.__actor_lookup_table__.get(urn)
    if location:
      del self.__actor_lookup_table__[urn]
      vector = location.get('vector')
      node = location.get('node')
      vector.remove(node)

  def __update_lookup_table__(self, vector, node):
    '''
    Updates a lookup table used for O(1) timer removal.
    '''
    urn = node.value.get_observer().actor_urn
    location = {
      'vector': vector,
      'node': node
    }
    self.__actor_lookup_table__.update({urn: location})

  def __vector1_insert__(self, timer):
    '''
    Inserts a timer into vector 1.

    Arguments: timer - The timer to be inserted.
    '''
    vector = self.__timer_vector1__
    bucket = timer.get_expires() / 100 - 1
    node = vector[bucket].append(timer)
    self.__update_lookup_table__(vector[bucket], node)

  def __vector2_insert__(self, timer):
    '''
    Inserts a timer into vector 2.

    Arguments: timer - The timer to be inserted.
    '''
    vector = self.__timer_vector2__
    bucket = timer.get_expires() / 25600 - 1
    node = vector[bucket].append(timer)
    self.__update_lookup_table__(vector[bucket], node)

  def __vector3_insert__(self, timer):
    '''
    Inserts a timer into vector 3.

    Arguments: timer - The timer to be inserted.
    '''
    vector = self.__timer_vector3__
    bucket = timer.get_expires() / 6553600 - 1
    node = vector[bucket].append(timer)
    self.__update_lookup_table__(vector[bucket], node)

  def __vector4_insert__(self, timer):
    '''
    Inserts a timer into vector 4.

    Arguments: timer - The timer to be inserted.
    '''
    vector = self.__timer_vector4__
    bucket = timer.get_expires() / 1677721600 - 1
    node = vector[bucket].append(timer)
    self.__update_lookup_table__(vector[bucket], node)

  def on_failure(self, exception_type, exception_value, traceback):
    '''
    Logs exceptions for the TimerService.
    '''
    self.__logger__.error(exception_value)

  def on_receive(self, message):
    '''
    Handles incoming messages.

    Arguments: message - The message to be processed.
    '''
    # This is necessary because all Pykka messages
    # must be of type dict.
    message = message.get('content')
    if not message:
      return
    # Handle the message.
    if isinstance(message, ReceiveTimeoutCommand):
      uuid = message.get_sender().actor_urn
      if not self.__actor_lookup_table__.has_key(uuid):
        timeout = message.get_timeout()
        observer = message.get_sender()
        recurring = message.is_recurring()
        timer = TimerService.Timer(observer, timeout, recurring)
        self.__schedule__(timer)
      else:
        self.__logger__.warning('Actor %s is requesting too many simultaneous timers.'
          % uuid)
    elif isinstance(message, StopTimeoutCommand):
      self.__unschedule__(message)
    elif isinstance(message, ClockEvent):
      self.__tick__()

  def on_start(self):
    '''
    Initialized the TimerService.
    '''
    self.__clock__ = MonotonicClock(self.actor_ref, TimerService.TICK_SIZE)
    self.__clock__.start()

  def on_stop(self):
    '''
    Cleans up after TimerService.
    '''
    self.__clock__.stop()

  class Timer(object):
    def __init__(self, observer, timeout, recurring = False):
      self.__observer__ = observer
      self.__recurring__ = recurring
      self.__timeout__ = timeout
      self.__expires__ = 0

    def get_expires(self):
      return self.__expires__

    def get_observer(self):
      return self.__observer__

    def get_timeout(self):
      return self.__timeout__

    def is_recurring(self):
      return self.__recurring__

    def set_expires(self, expires):
      self.__expires__ = expires
