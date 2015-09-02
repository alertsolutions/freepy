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
#
# Cristian Groza <frontc18@gmail.com>

from freepy.lib.commands import *
from unittest import TestCase, expectedFailure

class BackgroundCommandTests(TestCase):
  def test_success_scenario(self):
    command = BackgroundCommand(object())

class UUIDCommandTests(TestCase):
  def test_failed_scenario_no_variables(self):
    self.assertRaises(ValueError, UUIDCommand, None, None)

class ACLCheckCommandTests(TestCase):
	def test_success_scenario(self):
		command = ACLCheckCommand(object(), ip = '192.168.1.1', list_name = 'lan')
		desired_output = 'bgapi acl 192.168.1.1 lan\nJob-UUID: %s\n\n' % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

	def test_failed_scenario_no_variables(self):
		self.assertRaises(ValueError, ACLCheckCommand, object(), ip = None, list_name = None)

	def test_failed_scenario_no_variable_ip(self):
		self.assertRaises(ValueError, ACLCheckCommand, object(), ip = None, list_name = 'lan')

	def test_failed_scenario_no_variable_list_name(self):
		self.assertRaises(ValueError, ACLCheckCommand, object(), ip = '192.168.1.1', list_name = None)

class CheckUserGroupCommandTests(TestCase):
	def test_success_scenario(self):
		command = CheckUserGroupCommand(object(), user = 'test', domain = 'domain_test.com', group_name = 'groupname_test')
		desired_output = 'bgapi in_group test@domain_test.com groupname_test\nJob-UUID: %s\n\n'  % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

class DialedExtensionHupAllCommandTests(TestCase):
	def test_success_scenario(self):
		command = DialedExtensionHupAllCommand(object(), clearing = '999-999-9999', extension = '493')
		desired_output = 'bgapi fsctl hupall 999-999-9999 dialed_ext 493\nJob-UUID: %s\n\n' % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)
    
class DisableVerboseEventsCommandTests(TestCase):
	def test_success_scenario(self):
		command = DisableVerboseEventsCommand(object())
		desired_output = 'bgapi fsctl verbose_events off\nJob-UUID: %s\n\n' % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

class DomainExistsCommandTests(TestCase):
	def test_success_scenario(self):
		command = DomainExistsCommand(object(), domain = 'domain_test.com')
		desired_output = 'bgapi domain_exists domain_test.com\nJob-UUID: %s\n\n'  % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

class EnableVerboseEventsCommandTests(TestCase):
  def test_success_scenario(self):
    command = EnableVerboseEventsCommand(object())
    desired_output = 'bgapi fsctl verbose_events on\nJob-UUID: %s\n\n'  % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)

class GetDefaultDTMFDurationCommandTests(TestCase):
  def test_success_scenario(self):
    command = GetDefaultDTMFDurationCommand(object())
    desired_output = 'bgapi fsctl default_dtmf_duration 0\nJob-UUID: %s\n\n'  % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)
    
class GetGlobalVariableCommandTests(TestCase):
  def test_success_scenario(self):
    command = GetGlobalVariableCommand(object(), name='testVariable')   	
    desired_output = 'bgapi global_getvar testVariable\nJob-UUID: %s\n\n'  % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)

  def test_failed_scenario_no_variable(self):
  	self.assertRaises(ValueError, GetGlobalVariableCommand, object(), name = None)

class GetMaxSessionsCommandTests(TestCase):
  def test_success_scenario(self):
    command = GetMaxSessionsCommand(object())   	
    desired_output = 'bgapi fsctl max_sessions\nJob-UUID: %s\n\n'  % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)

class GetMaximumDTMFDurationCommandTests(TestCase):
  def test_success_scenario(self):
    command = GetMaximumDTMFDurationCommand(object())   	
    desired_output = 'bgapi fsctl max_dtmf_duration 0\nJob-UUID: %s\n\n'  % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)

class GetMinimumDTMFDurationCommandTests(TestCase):
  def test_success_scenario(self):
    command = GetMinimumDTMFDurationCommand(object())   	
    desired_output = 'bgapi fsctl min_dtmf_duration 0\nJob-UUID: %s\n\n'  % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)

class GetSessionsPerSecondCommandTests(TestCase):
  def test_success_scenario(self):
    command = GetSessionsPerSecondCommand(object())   	
    desired_output = 'bgapi fsctl last_sps\nJob-UUID: %s\n\n'  % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)

class GetGroupCallBridgeStringCommandTests(TestCase):
  def test_success_scenario_value_F(self):
    command = GetGroupCallBridgeStringCommand(object(), group = 'groupname_test', domain = 'domain_test.com', option = '+F')   	
    desired_output = 'bgapi group_call groupname_test@domain_test.com+F\nJob-UUID: %s\n\n'  % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)

  def test_failed_scenario_no_value_option(self):
  	self.assertRaises(ValueError, GetGroupCallBridgeStringCommand, object(), group = 'groupname_test', domain = 'domain_test.com', option = 'None')

  def test_success_scenario_value_A(self):
    command = GetGroupCallBridgeStringCommand(object(), group = 'groupname_test', domain = 'domain_test.com', option = '+A')   	
    desired_output = 'bgapi group_call groupname_test@domain_test.com+A\nJob-UUID: %s\n\n'  % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)
   
  def test_success_scenario_value_F(self):
    command = GetGroupCallBridgeStringCommand(object(), group = 'groupname_test', domain = 'domain_test.com', option = '+E')   	
    desired_output = 'bgapi group_call groupname_test@domain_test.com+E\nJob-UUID: %s\n\n'  % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)

  def test_failed_scenario_bad_variable(self):
    self.assertRaises(ValueError, GetGroupCallBridgeStringCommand, object(), group = 'groupname_test', domain = 'domain_test.com', option = '+G')
 
class HupAllCommandTests(TestCase):
  def test_success_scenario(self):
    command = HupAllCommand(object(), cause = 'test_cause', var_name = 'test_var_name', var_value = 'test_var_value')   	
    desired_output = 'bgapi hupall test_cause test_var_name test_var_value\nJob-UUID: %s\n\n'  % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)
 
class LoadModuleCommandTests(TestCase):
  def test_success_scenario(self):
    command = LoadModuleCommand(object(), name = "testModule")
    desired_output = 'bgapi load testModule\nJob-UUID: %s\n\n'  % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)
     
class OriginateCommandTests(TestCase):
  def test_success_scenario(self):
    command = OriginateCommand(object(), url = "http://test.com", extension = None, app_name = 'appTestme', app_args = ['arg1','arg2'], options = ['opt1','opt2'])
    desired_output = 'bgapi originate {opt1,opt2}http://test.com &appTestme(arg1 arg2)\nJob-UUID: %s\n\n'  % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)
    
class PauseSessionCreationCommandTests(TestCase):
  def test_success_scenario(self):
    command = PauseSessionCreationCommand(object(), direction = "testDirection")
    desired_output = 'bgapi fsctl pause testDirection\nJob-UUID: %s\n\n'  % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)

class ReclaimMemoryCommandTests(TestCase):
  def test_success_scenario(self):
    command = ReclaimMemoryCommand(object())
    desired_output = 'bgapi fsctl reclaim_mem\nJob-UUID: %s\n\n'  % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)

class ResumeSessionCreationCommandTests(TestCase):
  def test_success_scenario_passvariable(self):
    command = ResumeSessionCreationCommand(object(), direction = "testDirection")
    desired_output = 'bgapi fsctl resume testDirection\nJob-UUID: %s\n\n'  % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)
   	
  def test_success_scenario_novariable(self):
    command = ResumeSessionCreationCommand(object())
    desired_output = 'bgapi fsctl resume\nJob-UUID: %s\n\n'  % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)

class SetDefaultDTMFDurationCommandTests(TestCase):
  def test_success_scenario(self):
    command = SetDefaultDTMFDurationCommand(object(), duration = 500)
    desired_output = 'bgapi fsctl default_dtmf_duration 500\nJob-UUID: %s\n\n'  % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)

class SetGlobalVariableCommandTests(TestCase):
  def test_success_scenario(self):
    command = SetGlobalVariableCommand(object(), name = 'testName', value = 'testValue')
    desired_output = 'bgapi global_setvar testName=testValue\nJob-UUID: %s\n\n'  % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)

class SetMaximumDTMFDurationCommandTests(TestCase):
	def test_success_scenario(self):
		command = SetMaximumDTMFDurationCommand(object(), duration = 500)
		desired_output = 'bgapi fsctl max_dtmf_duration 500\nJob-UUID: %s\n\n'  % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

class SetMinimumDTMFDurationCommandTests(TestCase):
	def test_success_scenario(self):
		command = SetMinimumDTMFDurationCommand(object(), duration = 500)
		desired_output = 'bgapi fsctl min_dtmf_duration 500\nJob-UUID: %s\n\n'  % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

class SetSessionsPerSecondCommandTests(TestCase):
	def test_success_scenario(self):
		command = SetSessionsPerSecondCommand(object(), sessions_per_second = 15)
		desired_output = 'bgapi fsctl sps 15\nJob-UUID: %s\n\n'  % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

class ShutdownCommandTests(TestCase):
	def test_success_scenario_value_elegant(self):
		command = ShutdownCommand(object(), option = 'elegant')
		desired_output = 'bgapi fsctl shutdown elegant\nJob-UUID: %s\n\n'  % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

	def test_success_scenario_value_asap(self):
		command = ShutdownCommand(object(), option = 'asap')
		desired_output = 'bgapi fsctl shutdown asap\nJob-UUID: %s\n\n'  % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

	def test_success_scenario_value_restart(self):
		command = ShutdownCommand(object(), option = 'restart')
		desired_output = 'bgapi fsctl shutdown restart\nJob-UUID: %s\n\n'  % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

	def test_success_scenario_value_restart(self):
		command = ShutdownCommand(object(), option = 'cancel')
		desired_output = 'bgapi fsctl shutdown cancel\nJob-UUID: %s\n\n'  % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

	def test_failed_scenario_with_no_value(self):
		self.assertRaises(ValueError, ShutdownCommand, object(), option = 'n/a')

class StatusCommandTests(TestCase):
	def test_success_scenario(self):
		command = StatusCommand(object())
		desired_output = 'bgapi status\nJob-UUID: %s\n\n'  % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)
    
class SyncClockCommandTests(TestCase):
	def test_success_scenario(self):
		command = SyncClockCommand(object())
		desired_output = 'bgapi fsctl sync_clock\nJob-UUID: %s\n\n'  % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

class SyncClockWhenIdleCommandTests(TestCase):
	def test_success_scenario(self):
		command = SyncClockWhenIdleCommand(object())
		desired_output = 'bgapi fsctl sync_clock_when_idle\nJob-UUID: %s\n\n'  % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

class UnloadModuleCommandTests(TestCase):
	def test_success_scenario_passvariables(self):
		command = UnloadModuleCommand(object(), name = 'testName', force = 'true')
		desired_output = 'bgapi unload -f testName\nJob-UUID: %s\n\n'  % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)
   
	def test_success_scenario_passvariable(self):
		command = UnloadModuleCommand(object(), name = 'testName')
		desired_output = 'bgapi unload testName\nJob-UUID: %s\n\n'  % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

class AnswerCommandTests(TestCase):
	def test_success_scenario(self):
		command = AnswerCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079')
		desired_output = 'bgapi uuid_answer 21516b8e-5a0b-485a-9e53-933e42947079\nJob-UUID: %s\n\n'  % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

class BreakCommandTests(TestCase):
	def test_success_scenario(self):
		command = BreakCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079')
		desired_output = 'bgapi uuid_break 21516b8e-5a0b-485a-9e53-933e42947079\nJob-UUID: %s\n\n' % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

class BridgeCommandTests(TestCase):
	def test_success_scenario(self):
		command = BridgeCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079', other_uuid = '21516b8e-5a0b-485a-9e53-933e42947666')
		desired_output = 'bgapi uuid_bridge 21516b8e-5a0b-485a-9e53-933e42947079 21516b8e-5a0b-485a-9e53-933e42947666\nJob-UUID: %s\n\n' % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

	def test_failed_scenario_no_variable_other_uuid(self):
		self.assertRaises(ValueError, BridgeCommand, object(), '21516b8e-5a0b-485a-9e53-933e42947079', other_uuid = None)

class BroadcastCommandTests(TestCase):
	def test_success_scenario_withPath(self):
		command = BroadcastCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079', leg = 'aleg', path = 'testPath', app_name = None, app_args = 'app_args')
		desired_output = 'bgapi uuid_broadcast 21516b8e-5a0b-485a-9e53-933e42947079 testPath aleg\nJob-UUID: %s\n\n'  % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

	def test_success_scenario_withAppName(self):
		command = BroadcastCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079', leg = 'aleg', path = None, app_name = 'testApp', app_args = 'app_args')
		desired_output = 'bgapi uuid_broadcast 21516b8e-5a0b-485a-9e53-933e42947079 testApp::app_args aleg\nJob-UUID: %s\n\n'  % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

	def test_success_scenario_variable_leg_value_aleg(self):
		command = BroadcastCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079', leg = 'aleg', path = 'testPath', app_name = None, app_args = 'app_args')
		desired_output = 'bgapi uuid_broadcast 21516b8e-5a0b-485a-9e53-933e42947079 testPath aleg\nJob-UUID: %s\n\n'  % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

	def test_success_scenario_variable_leg_value_bleg(self):
		command = BroadcastCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079', leg = 'bleg', path = 'testPath', app_name = None, app_args = 'app_args')
		desired_output = 'bgapi uuid_broadcast 21516b8e-5a0b-485a-9e53-933e42947079 testPath bleg\nJob-UUID: %s\n\n'  % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

	def test_success_scenario_variable_leg_value_both(self):
		command = BroadcastCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079', leg = 'both', path = 'testPath', app_name = None, app_args = 'app_args')
		desired_output = 'bgapi uuid_broadcast 21516b8e-5a0b-485a-9e53-933e42947079 testPath both\nJob-UUID: %s\n\n'  % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

	def test_failed_scenario_no_variable_leg(self):
		self.assertRaises(ValueError, BroadcastCommand, object(), '21516b8e-5a0b-485a-9e53-933e42947079', leg = None, path = 'testPath', app_name = None, app_args = 'app_args')

	def test_failed_scenario_runtime(self):
		self.assertRaises(RuntimeError, BroadcastCommand, object(), '21516b8e-5a0b-485a-9e53-933e42947079', leg = 'bleg', path = 'testPath', app_name = 'testApp', app_args = 'app_args')

class ChatCommandTests(TestCase):
	def test_success_scenario(self):
		command = ChatCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079', text = None)
		desired_output = 'bgapi uuid_chat 21516b8e-5a0b-485a-9e53-933e42947079 None\nJob-UUID: %s\n\n' % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)    

class DeflectCommandTests(TestCase):
	def test_success_scenario(self):
		command = DeflectCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079', url = 'testURL')
		desired_output = 'bgapi uuid_deflect 21516b8e-5a0b-485a-9e53-933e42947079 testURL\nJob-UUID: %s\n\n' % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)    

class DisableMediaCommandTests(TestCase):
	def test_success_scenario(self):
		command = DisableMediaCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079')
		desired_output = 'bgapi uuid_media off 21516b8e-5a0b-485a-9e53-933e42947079\nJob-UUID: %s\n\n' % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)    

class DisplayCommandTests(TestCase):
	def test_success_scenario(self):
		command = DisplayCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079', display = 'MessageBox.Show()')
		desired_output = 'bgapi uuid_display 21516b8e-5a0b-485a-9e53-933e42947079 MessageBox.Show()\nJob-UUID: %s\n\n' % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)    

class DualTransferCommandTests(TestCase):
	def test_success_scenario(self):
		command = DualTransferCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079', extension_a = '0', extension_b = '1', dialplan_a = 'plana', dialplan_b = 'planb', context_a = 'contxa', context_b = 'contxb')
		desired_output = 'bgapi uuid_dual_transfer 21516b8e-5a0b-485a-9e53-933e42947079 0/plana/contxa 1/planb/contxb\nJob-UUID: %s\n\n' % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

	def test_failed_scenario_without_variable(self):
		self.assertRaises(RuntimeError, DualTransferCommand, object(), '21516b8e-5a0b-485a-9e53-933e42947079', extension_a = None, extension_b = None)    

class DumpCommandTests(TestCase):
	def test_success_scenario(self):
		command = DumpCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079', format = None)
		desired_output = 'bgapi uuid_dump 21516b8e-5a0b-485a-9e53-933e42947079 None\nJob-UUID: %s\n\n' % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)    

class EarlyOkayCommandTests(TestCase):
	def test_success_scenario(self):
		command = EarlyOkayCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079')
		desired_output = 'bgapi uuid_early_ok 21516b8e-5a0b-485a-9e53-933e42947079\nJob-UUID: %s\n\n' % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

class EnableMediaCommandTests(TestCase):
	def test_success_scenario(self):
		command = EnableMediaCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079')
		desired_output = 'bgapi uuid_media 21516b8e-5a0b-485a-9e53-933e42947079\nJob-UUID: %s\n\n' % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

class EnableSessionHeartbeatCommandTests(TestCase):
	def test_success_scenario_with_variable(self):
		command = EnableSessionHeartbeatCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079', start_time = 60)
		desired_output = 'bgapi uuid_session_heartbeat 21516b8e-5a0b-485a-9e53-933e42947079 sched 60\nJob-UUID: %s\n\n' % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

	def test_success_scenario_without_variable(self):
		command = EnableSessionHeartbeatCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079')
		desired_output = 'bgapi uuid_session_heartbeat 21516b8e-5a0b-485a-9e53-933e42947079\nJob-UUID: %s\n\n' % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

class FileManagerCommandTests(TestCase):
  def test_success_scenario_with_variable_speed(self):
    command = FileManagerCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079', command = 'speed')
    desired_output = 'bgapi uuid_fileman 21516b8e-5a0b-485a-9e53-933e42947079 speed\nJob-UUID: %s\n\n' % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)

  def test_success_scenario_with_variable_pause(self):
    command = FileManagerCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079', command = 'pause')
    desired_output = 'bgapi uuid_fileman 21516b8e-5a0b-485a-9e53-933e42947079 pause\nJob-UUID: %s\n\n' % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)

  def test_success_scenario_with_variable_truncate(self):
    command = FileManagerCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079', command = 'truncate')
    desired_output = 'bgapi uuid_fileman 21516b8e-5a0b-485a-9e53-933e42947079 truncate\nJob-UUID: %s\n\n' % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)

  def test_success_scenario_with_variable_volume(self):
    command = FileManagerCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079', command = 'volume')
    desired_output = 'bgapi uuid_fileman 21516b8e-5a0b-485a-9e53-933e42947079 volume\nJob-UUID: %s\n\n' % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)

  def test_success_scenario_with_variable_restart(self):
    command = FileManagerCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079', command = 'restart')
    desired_output = 'bgapi uuid_fileman 21516b8e-5a0b-485a-9e53-933e42947079 restart\nJob-UUID: %s\n\n' % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)

  def test_success_scenario_with_variable_seek(self):
    command = FileManagerCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079', command = 'seek')
    desired_output = 'bgapi uuid_fileman 21516b8e-5a0b-485a-9e53-933e42947079 seek\nJob-UUID: %s\n\n' % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)

  def test_failed_scenario_without_variable(self):
    self.assertRaises(ValueError, FileManagerCommand, object(), '21516b8e-5a0b-485a-9e53-933e42947079', command = None)

class FlushDTMFCommandTests(TestCase):
	def test_success_scenario(self):
		command = FlushDTMFCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079')
		desired_output = 'bgapi uuid_flush_dtmf 21516b8e-5a0b-485a-9e53-933e42947079\nJob-UUID: %s\n\n' % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

class GetAudioLevelCommandTests(TestCase):
	def test_success_scenario(self):
		command = GetAudioLevelCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079')
		desired_output = 'bgapi uuid_audio 21516b8e-5a0b-485a-9e53-933e42947079 start read level\nJob-UUID: %s\n\n' % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

class GetBugListCommandTests(TestCase):
	def test_success_scenario(self):
		command = GetBugListCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079')
		desired_output = 'bgapi uuid_buglist 21516b8e-5a0b-485a-9e53-933e42947079\nJob-UUID: %s\n\n' % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

class GetVariableCommandTests(TestCase):
	def test_success_scenario(self):
		command = GetVariableCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079', name = 'testName')
		desired_output = 'bgapi uuid_getvar 21516b8e-5a0b-485a-9e53-933e42947079 testName\nJob-UUID: %s\n\n' % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

	def test_failed_scenario_without_variable(self):
		self.assertRaises(ValueError, GetVariableCommand, object(), '21516b8e-5a0b-485a-9e53-933e42947079', name = None)

class HoldCommandTests(TestCase):
	def test_success_scenario(self):
		command = HoldCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079')
		desired_output = 'bgapi uuid_hold 21516b8e-5a0b-485a-9e53-933e42947079\nJob-UUID: %s\n\n' % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

class KillCommandTests(TestCase):
	def test_success_scenario_with_variable(self):
		command = KillCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079', cause = 'fake cause')
		desired_output = 'bgapi uuid_kill 21516b8e-5a0b-485a-9e53-933e42947079 fake cause\nJob-UUID: %s\n\n' % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

	def test_success_scenario_without_variable(self):
		command = KillCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079')
		desired_output = 'bgapi uuid_kill 21516b8e-5a0b-485a-9e53-933e42947079\nJob-UUID: %s\n\n' % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

class LimitCommandTests(TestCase):
	def test_success_scenario(self):
		command = LimitCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079', backend = 'backend', realm = 'realm', resource='resource', max_calls = 2, interval = 20, number = 15, dialplan = 'c', context='unknown')
		desired_output = 'bgapi uuid_limit 21516b8e-5a0b-485a-9e53-933e42947079 backend realm resource 2/20 15 c unknown\nJob-UUID: %s\n\n' % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)
   
class ParkCommandTests(TestCase):
	def test_success_scenario(self):
		command = ParkCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079')
		desired_output = 'bgapi uuid_park 21516b8e-5a0b-485a-9e53-933e42947079\nJob-UUID: %s\n\n' % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

class PauseCommandTests(TestCase):
	def test_success_scenario(self):
		command = PauseCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079')
		desired_output = 'bgapi pause 21516b8e-5a0b-485a-9e53-933e42947079 on\nJob-UUID: %s\n\n' % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

class PreProcessCommandTests(TestCase):
	def test_success_scenario(self):
		command = PreProcessCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079')
		desired_output = 'bgapi uuid_preprocess 21516b8e-5a0b-485a-9e53-933e42947079\nJob-UUID: %s\n\n' % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

class PreAnswerCommandTests(TestCase):
	def test_success_scenario(self):
		command = PreAnswerCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079')
		desired_output = 'bgapi uuid_preanswer 21516b8e-5a0b-485a-9e53-933e42947079\nJob-UUID: %s\n\n' % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

class ReceiveDTMFCommandTests(TestCase):
  def test_success_scenario(self):
    command = ReceiveDTMFCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079')
    desired_output = 'bgapi uuid_recv_dtmf 21516b8e-5a0b-485a-9e53-933e42947079 None\nJob-UUID: %s\n\n' % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)

class RenegotiateMediaCommandTests(TestCase):
	def test_success_scenario(self):
		command = RenegotiateMediaCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079', codec = 'test_codex94')
		desired_output = 'bgapi uuid_media_reneg 21516b8e-5a0b-485a-9e53-933e42947079 =test_codex94\nJob-UUID: %s\n\n' % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

class SendDTMFCommandTests(TestCase):
	def test_success_scenario(self):
		command = SendDTMFCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079')
		desired_output = 'bgapi uuid_send_dtmf 21516b8e-5a0b-485a-9e53-933e42947079 None\nJob-UUID: %s\n\n' % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

class SendInfoCommandTests(TestCase):
	def test_success_scenario(self):
		command = SendInfoCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079')
		desired_output = 'bgapi uuid_send_info 21516b8e-5a0b-485a-9e53-933e42947079\nJob-UUID: %s\n\n' % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

class SetAudioLevelCommandTests(TestCase):
	def test_success_scenario_with_variable(self):
		command = SetAudioLevelCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079', level = 3.3)
		desired_output = 'bgapi uuid_audio 21516b8e-5a0b-485a-9e53-933e42947079 start write level 3.300000\nJob-UUID: %s\n\n' % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

	def test_failed_scenario_with_invalid_variable_high(self):
		self.assertRaises(ValueError, SetAudioLevelCommand, object(), '21516b8e-5a0b-485a-9e53-933e42947079', level = 4.1)

	def test_failed_scenario_with_invalid_variable_low(self):
		self.assertRaises(ValueError, SetAudioLevelCommand, object(), '21516b8e-5a0b-485a-9e53-933e42947079', level = -4.1)

class SetMultipleVariableCommandTests(TestCase):
	def test_success_scenario(self):
		command = SetMultipleVariableCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079', variables = dict([('49','55')]))
		desired_output = 'bgapi uuid_setvar_multi 21516b8e-5a0b-485a-9e53-933e42947079 4=9\nJob-UUID: %s\n\n' % command.__job_uuid__
		self.assertTrue(str(command) == desired_output)

class SetVariableCommandTests(TestCase):
  def test_success_scenario(self):
    command = SetVariableCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079', name = 'testName', value = 'testValue')   	
    desired_output = 'bgapi uuid_setvar 21516b8e-5a0b-485a-9e53-933e42947079 testName testValue\nJob-UUID: %s\n\n' % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)

class SimplifyCommandTests(TestCase):
  def test_success_scenario(self):
    command = SimplifyCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079', name = 'testName', value = 'testValue')   	
    desired_output = 'bgapi uuid_simplify 21516b8e-5a0b-485a-9e53-933e42947079\nJob-UUID: %s\n\n' % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)
 
class StartDebugMediaCommandTests(TestCase):
  def test_success_scenario(self):
    command = StartDebugMediaCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079', option = 'testOption')   	
    desired_output = 'bgapi uuid_debug_media 21516b8e-5a0b-485a-9e53-933e42947079 testOption on\nJob-UUID: %s\n\n' % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)
 
class StartDisplaceCommandTests(TestCase):
  def test_success_scenario(self):
    command = StartDisplaceCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079', path = 'testPath', limit = 450, mux='testMux')   	
    desired_output = 'bgapi uuid_displace 21516b8e-5a0b-485a-9e53-933e42947079 start testPath 450 mux\nJob-UUID: %s\n\n' % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)
 
class StopDebugMediaCommandTests(TestCase):
  def test_success_scenario(self):
    command = StopDebugMediaCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079')
    desired_output = 'bgapi uuid_debug_media 21516b8e-5a0b-485a-9e53-933e42947079 off\nJob-UUID: %s\n\n' % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)

class StopDisplaceCommandTests(TestCase):
  def test_success_scenario(self):
    command = StopDisplaceCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079')
    desired_output = 'bgapi uuid_displace 21516b8e-5a0b-485a-9e53-933e42947079 stop\nJob-UUID: %s\n\n' % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)

class TransferCommandTests(TestCase):
  def test_success_scenario(self):
    command = TransferCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079', leg = 'legTest', extension = '384', dialplan = '44', context = 'contextTest')
    desired_output = 'bgapi uuid_transfer 21516b8e-5a0b-485a-9e53-933e42947079 legTest 384 44 contextTest\nJob-UUID: %s\n\n' % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)

class UnholdCommandTests(TestCase):
  def test_success_scenario(self):
    command = UnholdCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079')   	
    desired_output = 'bgapi uuid_hold off 21516b8e-5a0b-485a-9e53-933e42947079\nJob-UUID: %s\n\n' % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)
 
class UnpauseCommandTests(TestCase):
  def test_success_scenario(self):
    command = UnpauseCommand(object(), '21516b8e-5a0b-485a-9e53-933e42947079')   	
    desired_output = 'bgapi pause 21516b8e-5a0b-485a-9e53-933e42947079 off\nJob-UUID: %s\n\n' % command.__job_uuid__
    self.assertTrue(str(command) == desired_output)
 