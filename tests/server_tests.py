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

from freepy.lib.core import *
from freepy.lib.server import *
from pykka import ActorRegistry, ThreadingActor
from unittest import TestCase

class AuthCommandTests(TestCase):
  def test_success_scenario(self):
    command = AuthCommand('ClueCon')
    self.assertTrue(str(command) == 'auth ClueCon\n\n')

class EventsCommandTests(TestCase):
  def test_success_scenario_with_multiple_events(self):
    command = EventsCommand(['BACKGROUND_JOB', 'HEARTBEAT'])
    self.assertTrue(str(command) == 'event plain BACKGROUND_JOB HEARTBEAT\n\n')

  def test_success_scenario_with_single_event(self):
    command = EventsCommand(['BACKGROUND_JOB'])
    self.assertTrue(str(command) == 'event plain BACKGROUND_JOB\n\n')

  def test_invalid_format(self):
    self.assertRaises(ValueError, EventsCommand, ['BACKGROUD_JOB'], format = 'invalid')

class TestApplicationFactoryActor(ThreadingActor):
  def on_receive(self, message):
    pass

class ApplicationFactoryTests(TestCase):
  __test_actor_path__ = 'tests.server_tests.TestApplicationFactoryActor'

  @classmethod
  def tearDownClass(cls):
    ActorRegistry.stop_all()

  def test_class_instantiation(self):
    self.__factory__ = ApplicationFactory(object())
    self.__factory__.register(self.__test_actor_path__)
    instance_a = self.__factory__.get_instance(self.__test_actor_path__)
    instance_b = self.__factory__.get_instance(self.__test_actor_path__)
    self.assertFalse(instance_a.actor_urn == instance_b.actor_urn)
    self.__factory__.shutdown()

  def test_singleton_instantiation(self):
    self.__factory__ = ApplicationFactory(object())
    self.__factory__.register(self.__test_actor_path__, type = 'singleton')
    instance_a = self.__factory__.get_instance(self.__test_actor_path__)
    instance_b = self.__factory__.get_instance(self.__test_actor_path__)
    self.assertTrue(instance_a.actor_urn == instance_b.actor_urn)
    self.__factory__.shutdown()

  def test_different_types_same_name_fail(self):
    self.__factory__ = ApplicationFactory(object())
    self.__factory__.register(self.__test_actor_path__, type = 'singleton')
    self.assertRaises(ValueError, self.__factory__.register, self.__test_actor_path__)
