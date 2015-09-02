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

# Cristian Groza <frontc18@gmail.com>

from uuid import uuid4

# Import the proper StringIO implementation.
try:
  from cStringIO import StringIO
except:
  from StringIO import StringIO

class BackgroundCommand(object):
  def __init__(self, *args, **kwargs):
    self.__sender__ = args[0]
    self.__job_uuid__ = uuid4().get_urn().split(':', 2)[2]
    if not self.__sender__:
      raise ValueError('The sender parameter must be a valid reference to a Pykka actor.')

  def get_job_uuid(self):
    return self.__job_uuid__

  def get_sender(self):
    return self.__sender__

class UUIDCommand(BackgroundCommand):
  def __init__(self, *args, **kwargs):
    super(UUIDCommand, self).__init__(*args, **kwargs)
    self.__uuid__ = args[1]
    if not self.__uuid__:
      raise ValueError('The value of uuid must be a valid UUID.')

  def get_uuid(self):
    return self.__uuid__

class ACLCheckCommand(BackgroundCommand):
  '''
  The ACLCheckCommand compares an ip to an ACL list.

  Arguments: sender - The freepy actor sending this command.
             ip - Internet Protocol address.
             list_name - ACL list name.
  '''
  def __init__(self, *args, **kwargs):
    super(ACLCheckCommand, self).__init__(*args, **kwargs)
    self.__ip__ = kwargs.get('ip')
    self.__list_name__ = kwargs.get('list_name')
    
    if not self.__ip__ :
      raise ValueError('The ip value %s is invalid' % self.__ip__)
    if not self.__list_name__ :
      raise ValueError('The list name value %s is invalid' % self.__list_name__)
    
  def get_ip(self):
    return self.__ip__

  def get_list_name(self):
    return self.__list_name__

  def __str__(self):
    return 'bgapi acl %s %s\nJob-UUID: %s\n\n' % (self.__ip__,
      self.__list_name__, self.__job_uuid__)

class AnswerCommand(UUIDCommand):
  '''
  The AnswerCommand answers a channel.

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
  '''
  def __init__(self, *args, **kwargs):
    super(AnswerCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi uuid_answer %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class BreakCommand(UUIDCommand):
  '''
  Break out of media being sent to a channel. For example, if an audio file is being played to a channel, 
  issuing uuid_break will discontinue the media and the call will move on in the dialplan, script, 
  or whatever is controlling the call.

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
              stop_all - boolean flag.*

  *If the stop_all flag is used then all audio files/prompts/etc. that are queued up to be played to the channel 
  will be removed, whereas without the all flag only the currently playing file will be discontinued. 
  '''
  def __init__(self, *args, **kwargs):
    super(BreakCommand, self).__init__(*args, **kwargs)
    self.__stop_all__ = kwargs.get('stop_all', False)

  def stop_all(self):
    return self.__stop_all__

  def __str__(self):
    if not self.__stop_all__:
      return 'bgapi uuid_break %s\nJob-UUID: %s\n\n' % (self.__uuid__,
        self.__job_uuid__)
    else:
      return 'bgapi uuid_break %s all\nJob-UUID: %s\n\n' % (self.__uuid__,
        self.__job_uuid__)

class BridgeCommand(UUIDCommand):
  '''
  Bridge two call legs together. Bridge needs atleast any one leg to be answered. 
  
  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
              other_uuid - universal unique identifier to Bridge.
  '''
  def __init__(self, *args, **kwargs):
    super(BridgeCommand, self).__init__(*args, **kwargs)
    self.__other_uuid__ = kwargs.get('other_uuid')
    if not self.__other_uuid__:
      raise ValueError('The value of other_uuid must be a valid UUID.')

  def get_other_uuid(self):
    return self.__other_uuid__

  def __str__(self):
    return 'bgapi uuid_bridge %s %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__other_uuid__, self.__job_uuid__)

class BroadcastCommand(UUIDCommand):
  '''
  Execute an arbitrary dialplan application on a specific <uuid>. 
  If a filename is specified then it is played into the channel(s).
  To execute an application use <app_name> and <app_args> syntax.

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
              leg - select which leg(s) to use [aleg|bleg|both].
              path - the path to the audio file to be played into the channels.*
              app_name - application name to be executed on the channel(s).*2
              app_args - arguments to the application(s) being executed on the channel(s).
  
  * Can provide path Or app_name, but not both. 
  '''
  def __init__(self, *args, **kwargs):
    super(BroadcastCommand, self).__init__(*args, **kwargs)
    self.__leg__ = kwargs.get('leg')
    if not self.__leg__ or not self.__leg__ == 'aleg' and \
      not self.__leg__ == 'bleg' and not self.__leg__ == 'both':
      raise ValueError('The leg value %s is invalid' % self.__leg__)
    self.__path__ = kwargs.get('path')
    self.__app_name__ = kwargs.get('app_name')
    self.__app_args__ = kwargs.get('app_args')
    if self.__path__ and self.__app_name__:
      raise RuntimeError('A broadcast command can specify either a path \
      or an app_name but not both.')

  def get_leg(self):
    return self.__leg__

  def get_path(self):
    return self.__path__

  def get_app_name(self):
    return self.__app_name__

  def get_app_args(self):
    return self.__app_args__

  def __str__(self):
    buffer = StringIO()
    buffer.write('bgapi uuid_broadcast %s ' % self.__uuid__)
    if self.__path__:
      buffer.write('%s' % self.__path__)
    else:
      buffer.write('%s' % self.__app_name__)
      if self.__app_args__:
        buffer.write('::%s' % self.__app_args__)
    buffer.write(' %s\nJob-UUID: %s\n\n' % (self.__leg__, self.__job_uuid__))
    try:
      return buffer.getvalue()
    finally:
      buffer.close()

class ChatCommand(UUIDCommand):
  '''
  Send a chat message. If the endpoint associated with the session 
  <uuid> has a receive_event handler, this message gets sent to that 
  session and is interpreted as an instant message. 
  
  Arguments:  sender - the freepy actor sending this command.
              uuid - universal unique identifier.
              text - message to be sent.
  '''
  def __init__(self, *args, **kwargs):
    super(ChatCommand, self).__init__(*args, **kwargs)
    self.__text__ = kwargs.get('text', '')

  def get_text(self):
    return self.__text__

  def __str__(self):
    return 'bgapi uuid_chat %s %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__text__, self.__job_uuid__)

class CheckUserGroupCommand(BackgroundCommand):
  '''
  Determine if a <user> is in a group. 

  Arguments: sender - the freepy actor sending this command.
             'user' - username.
             'domain' - domain name.
             'group_name' - group name.
  '''  
  def __init__(self, *args, **kwargs):
    super(CheckUserGroupCommand, self).__init__(*args, **kwargs)
    self.__user__ = kwargs.get('user')
    self.__domain__ = kwargs.get('domain')
    self.__group_name__ = kwargs.get('group_name')

  def get_domain(self):
    return self.__domain__

  def get_group_name(self):
    return self.__group_name__

  def get_user(self):
    return self.__user__

  def __str__(self):
    if not self.__domain__:
      return 'bgapi in_group %s %s\nJob-UUID: %s\n\n' % (self.__user__,
        self.__group_name__, self.__job_uuid__)
    else:
      return 'bgapi in_group %s@%s %s\nJob-UUID: %s\n\n' % (self.__user__,
        self.__domain__, self.__group_name__, self.__job_uuid__)

class DeflectCommand(UUIDCommand):
  '''
  Deflect an answered SIP call off of FreeSWITCH by sending the REFER method.
  Deflect waits for the final response from the far end to be reported. 
  It returns the sip fragment from that response as the text in the FreeSWITCH 
  response to uuid_deflect. If the far end reports the REFER was successful, 
  then FreeSWITCH will issue a bye on the channel. 
  
  Arguments:  sender - the freepy actor sending this command.
              uuid - universal unique identifier.
              url - SIP url.
  '''
  def __init__(self, *args, **kwargs):
    super(DeflectCommand, self).__init__(*args, **kwargs)
    self.__url__ = kwargs.get('url')

  def get_url(self):
    return self.__url__

  def __str__(self):
    return 'bgapi uuid_deflect %s %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__url__, self.__job_uuid__)

class DialedExtensionHupAllCommand(BackgroundCommand):
  '''
  Can be used to disconnect existing calls to an extension.

  Arguments: sender - The freepy actor sending this command.
             clearing - clearing type. 
             extension - extension number to be disconnected.
  '''  
  def __init__(self, *args, **kwargs):
    super(DialedExtensionHupAllCommand, self).__init__(*args, **kwargs)
    self.__clearing__ = kwargs.get('clearing')
    self.__extension__ = kwargs.get('extension')

  def get_clearing(self):
    return self.__clearing__

  def get_extension(self):
    return self.__extension__

  def __str__(self):
    return 'bgapi fsctl hupall %s dialed_ext %s\nJob-UUID: %s\n\n' % (self.__clearing__,
      self.__extension__, self.__job_uuid__)

class DisableMediaCommand(UUIDCommand):
  '''
  Reinvite FreeSWITCH out of the media path: 
  
  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
  '''
  def __init__(self, *args, **kwargs):
    super(DisableMediaCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi uuid_media off %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class DisableVerboseEventsCommand(BackgroundCommand):
  '''
  Disable verbose events. Verbose events have every channel variable in every event 
  for a particular channel. Non-verbose events have only the pre-selected channel 
  variables in the event headers. 

  Arguments: sender - The freepy actor sending this command.
  '''  
  def __init__(self, *args, **kwargs):
    super(DisableVerboseEventsCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi fsctl verbose_events off\nJob-UUID: %s\n\n' % self.__job_uuid__

class DisplayCommand(UUIDCommand):
  '''
  Updates the display on a phone if the phone supports this. This works on some SIP 
  phones right now including Polycom and Snom. This command makes the phone re-negotiate 
  the codec. The SIP -> RTP Packet Size should be 0.020. If it is set to 0.030 on the SPA 
  series phones it causes a DTMF lag. When DTMF keys are pressed on the phone they are can 
  be seen on the fs_cli 4-6 seconds late. 

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
              display - screen display.
  '''
  def __init__(self, *args, **kwargs):
    super(DisplayCommand, self).__init__(*args, **kwargs)
    self.__display__ = kwargs.get('display')

    def get_display(self):
      return self.__display__

  def __str__(self):
    return 'bgapi uuid_display %s %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__display__, self.__job_uuid__)

class DomainExistsCommand(BackgroundCommand):
  '''
  Check if a domain exists. 

  Arguments: sender - The freepy actor sending this command.
             domain - domain to check.
  '''  
  def __init__(self, *args, **kwargs):
    super(DomainExistsCommand, self).__init__(*args, **kwargs)
    self.__domain__ = kwargs.get('domain')

  def get_domain(self):
    return self.__domain__

  def __str__(self):
    return 'bgapi domain_exists %s\nJob-UUID: %s\n\n' % (self.__domain__,
      self.__job_uuid__)

class DualTransferCommand(UUIDCommand):
  '''
  Transfer each leg of a call to different destinations. 

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
              extension_a - target extension for aleg
              dialplan_a - target dialplan for aleg
              context_a - target context for aleg
              extension_b - target extension for bleg
              dialplan_b - target dialplan for bleg
              context_b - target context for bleg
  '''
  def __init__(self, *args, **kwargs):
    super(DualTransferCommand, self).__init__(*args, **kwargs)
    self.__extension_a__ = kwargs.get('extension_a')
    self.__extension_b__ = kwargs.get('extension_b')
    self.__dialplan_a__ = kwargs.get('dialplan_a')
    self.__dialplan_b__ = kwargs.get('dialplan_b')
    self.__context_a__ = kwargs.get('context_a')
    self.__context_b__ = kwargs.get('context_b')
    if not self.__extension_a__ and not self.__extension_b__:
      raise RuntimeError('A dual transer command requires the extension_a \
        and extension_b parameters to be provided.')

  def get_extension_a(self):
    return self.__extension_a__

  def get_extension_b(self):
    return self.__extension_b__

  def get_dialplan_a(self):
    return self.__dialplan_a__

  def get_dialplan_b(self):
    return self.__dialplan_b__

  def get_context_a(self):
    return self.__context_a__

  def get_context_b(self):
    return self.__context_b__

  def __str__(self):
    buffer = StringIO()
    buffer.write(self.__extension_a__)
    if self.__dialplan_a__:
      buffer.write('/%s' % self.__dialplan_a__)
    if self.__context_a__:
      buffer.write('/%s' % self.__context_a__)
    destination_a = buffer.getvalue()
    buffer.seek(0)
    buffer.write(self.__extension_b__)
    if self.__dialplan_b__:
      buffer.write('/%s' % self.__dialplan_b__)
    if self.__context_b__:
      buffer.write('/%s' % self.__context_b__)
    destination_b = buffer.getvalue()
    buffer.close()
    return 'bgapi uuid_dual_transfer %s %s %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      destination_a, destination_b, self.__job_uuid__)

class DumpCommand(UUIDCommand):
  '''
  Dumps all variable values for a session. 

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
              format - variable values output format. Default output XML.
  '''
  def __init__(self, *args, **kwargs):
    super(DumpCommand, self).__init__(*args, **kwargs)
    self.__format__ = kwargs.get('format', 'XML')

  def get_format(self):
    return self.__format__

  def __str__(self):
    return 'bgapi uuid_dump %s %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__format__, self.__job_uuid__)

class EarlyOkayCommand(UUIDCommand):
  '''
  Stops the process of ignoring early media, i.e. if ignore_early_media=true 
  it stops ignoring early media and responds normally. 

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
  '''
  def __init__(self, *args, **kwargs):
    super(EarlyOkayCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi uuid_early_ok %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class EnableMediaCommand(UUIDCommand):
  '''
  Reinvite FreeSWITCH into the media path: 

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
  '''
  def __init__(self, *args, **kwargs):
    super(EnableMediaCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi uuid_media %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class EnableSessionHeartbeatCommand(UUIDCommand):
  '''
  Enable session Heartbeat.

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
              start_time - seconds in the future to start.
  '''
  def __init__(self, *args, **kwargs):
    super(EnableSessionHeartbeatCommand, self).__init__(*args, **kwargs)
    self.__start_time__ = kwargs.get('start_time') # Seconds in the future to start

  def get_start_time(self):
    return self.__start_time__

  def __str__(self):
    if not self.__start_time__:
      return 'bgapi uuid_session_heartbeat %s\nJob-UUID: %s\n\n' % (self.__uuid__,
        self.__job_uuid__)
    else:
      return 'bgapi uuid_session_heartbeat %s sched %i\nJob-UUID: %s\n\n' % (self.__uuid__,
        self.__start_time__, self.__job_uuid__)

class EnableVerboseEventsCommand(BackgroundCommand):
  '''
  Enable verbose events. Verbose events have every channel variable in every event 
  for a particular channel. Non-verbose events have only the pre-selected channel 
  variables in the event headers. 

  Arguments: sender - The freepy actor sending this command.
  '''  

  def __init__(self, *args, **kwargs):
    super(EnableVerboseEventsCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi fsctl verbose_events on\nJob-UUID: %s\n\n' % self.__job_uuid__

class FileManagerCommand(UUIDCommand):
  '''
  Manage the audio being played into a channel from a sound file

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
              command - a parameter which controls what action should be taken*
              value - the value of the command**

  * Available Commands : 
  [speed]
  [volume]
  [pause]
  [stop]
  [truncate]
  [restart]
  [seek]
  ** Unit of measurement is milliseconds
  '''
  def __init__(self, *args, **kwargs):
    super(FileManagerCommand, self).__init__(*args, **kwargs)
    self.__command__ = kwargs.get('command')
    if not self.__command__ or not self.__command__ == 'speed' and \
      not self.__command__ == 'volume' and not self.__command__ == 'pause' and \
      not self.__command__ == 'stop' and not self.__command__ == 'truncate' and \
      not self.__command__ == 'restart' and not self.__command__ == 'seek':
      raise ValueError('The command parameter %s is invalid.' % self.__command__)
    self.__value__ = kwargs.get('value')

  def get_command(self):
    return self.__command__

  def get_value(self):
    return self.__value__

  def __str__(self):
    if self.__value__:
      return 'bgapi uuid_fileman %s %s:%s\nJob-UUID: %s\n\n' % (self.__uuid__,
        self.__command__, self.__value__, self.__job_uuid__)
    else:
      return 'bgapi uuid_fileman %s %s\nJob-UUID: %s\n\n' % (self.__uuid__,
        self.__command__, self.__job_uuid__)

class FlushDTMFCommand(UUIDCommand):
  '''
  Flush queued DTMF digits.

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
  '''
  def __init__(self, *args, **kwargs):
    super(FlushDTMFCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi uuid_flush_dtmf %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class GetAudioLevelCommand(UUIDCommand):
  '''
  Get the Audio Level 

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
  '''
  def __init__(self, *args, **kwargs):
    super(GetAudioLevelCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi uuid_audio %s start read level\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class GetBugListCommand(UUIDCommand):
  '''
  List the media bugs on channel.

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
  '''
  def __init__(self, *args, **kwargs):
    super(GetBugListCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi uuid_buglist %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class GetDefaultDTMFDurationCommand(BackgroundCommand):
  '''
  Gets the current value of default dtmf duration.

  Arguments: sender - The freepy actor sending this command.
  '''  
  def __init__(self, *args, **kwargs):
    super(GetDefaultDTMFDurationCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi fsctl default_dtmf_duration 0\nJob-UUID: %s\n\n' % self.__job_uuid__

class GetGlobalVariableCommand(BackgroundCommand):
  '''
  Gets the value of a global variable. 

  Arguments: sender - The freepy actor sending this command.
             name - the name of a global variable*

  * If the parameter is not provided then it gets all the global variables. 
  '''  
  def __init__(self, *args, **kwargs):
    super(GetGlobalVariableCommand, self).__init__(*args, **kwargs)
    self.__name__ = kwargs.get('name')
    if not self.__name__:
      raise ValueError('The name parameter is required.')

  def get_name(self):
    return self.__name__

  def __str__(self):
    return 'bgapi global_getvar %s\nJob-UUID: %s\n\n' % (self.__name__,
      self.__job_uuid__)

class GetMaxSessionsCommand(BackgroundCommand):
  '''
  Gets the value of the Maximum Sessions. 

  Arguments: sender - The freepy actor sending this command.
  '''  
  def __init__(self, *args, **kwargs):
    super(GetMaxSessionsCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi fsctl max_sessions\nJob-UUID: %s\n\n' % self.__job_uuid__

class GetMaximumDTMFDurationCommand(BackgroundCommand):
  '''
  Gets the current value of maximum dtmf duration.

  Arguments: sender - The freepy actor sending this command.
  '''  
  def __init__(self, *args, **kwargs):
    super(GetMaximumDTMFDurationCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi fsctl max_dtmf_duration 0\nJob-UUID: %s\n\n' % self.__job_uuid__

class GetMinimumDTMFDurationCommand(BackgroundCommand):
  '''
  Gets the current value of minimum dtmf duration.

  Arguments: sender - The freepy actor sending this command.
  '''  
  def __init__(self, *args, **kwargs):
    super(GetMinimumDTMFDurationCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi fsctl min_dtmf_duration 0\nJob-UUID: %s\n\n' % self.__job_uuid__

class GetSessionsPerSecondCommand(BackgroundCommand):
  '''
  Query the actual sessions-per-second. 

  Arguments: sender - The freepy actor sending this command.
  '''  
  def __init__(self, *args, **kwargs):
    super(GetSessionsPerSecondCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi fsctl last_sps\nJob-UUID: %s\n\n' % self.__job_uuid__

class GetVariableCommand(UUIDCommand):
  '''
  Get a variable from a channel. 

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
              name - the name of the variable to get from a channel
  '''
  def __init__(self, *args, **kwargs):
    super(GetVariableCommand, self).__init__(*args, **kwargs)
    self.__name__ = kwargs.get('name')
    if not self.__name__:
      raise ValueError('The name parameter is requied.')

  def get_name(self):
    return self.__name__

  def __str__(self):
    return 'bgapi uuid_getvar %s %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__name__, self.__job_uuid__)

class GetGroupCallBridgeStringCommand(BackgroundCommand):
  '''
  Returns the bridge string defined in a call group.

  Arguments: sender - The freepy actor sending this command.
             group - group name
             domain - domain name
             option - valid options [+F, +A, +E] *

  * +F
      will return the group members in a serial fashion (separated by |), 
    +A 
      will return them in a parallel fashion (separated by ,) 
    +E 
      will return them in a enterprise fashion (separated by :_:). 
  '''  

  def __init__(self, *args, **kwargs):
    super(GetGroupCallBridgeStringCommand, self).__init__(*args, **kwargs)
    self.__group__ = kwargs.get('group')
    self.__domain__ = kwargs.get('domain')
    self.__option__ = kwargs.get('option')
    if self.__option__ and not self.__option__ == '+F' and \
      not self.__option__ == '+A' and not self.__option__ == '+E':
      raise ValueError('The option parameter %s is invalid.' % self.__option__)

  def get_domain(self):
    return self.__domain__

  def get_group(self):
    return self.__group__

  def get_option(self):
    return self.__option__

  def __str__(self):
    if not self.__option__:
      return 'bgapi group_call %s@%s\nJob-UUID: %s\n\n' % (self.__group__,
        self.__domain__, self.__job_uuid__)
    else:
      return 'bgapi group_call %s@%s%s\nJob-UUID: %s\n\n' % (self.__group__,
        self.__domain__, self.__option__, self.__job_uuid__)

class HoldCommand(UUIDCommand):
  '''
  Place a call on hold. 

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
  '''
  def __init__(self, *args, **kwargs):
    super(HoldCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi uuid_hold %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class HupAllCommand(BackgroundCommand):
  '''
  Disconnect existing channels. 

  Arguments: sender - The freepy actor sending this command.
             cause - the reason.
             var_name - optional parameter variable name.
             var_value - optional parameter variable value. 
  '''  

  def __init__(self, *args, **kwargs):
    super(HupAllCommand, self).__init__(*args, **kwargs)
    self.__cause__ = kwargs.get('cause')
    self.__var_name__ = kwargs.get('var_name')
    self.__var_value__ = kwargs.get('var_value')

  def get_cause(self):
    return self.__cause__

  def get_variable_name(self):
    return self.__var_name__

  def get_variable_value(self):
    return self.__var_value__

  def __str__(self):
    if self.__var_name__ and self.__var_value__:
      return 'bgapi hupall %s %s %s\nJob-UUID: %s\n\n' % (self.__cause__,
        self.__var_name__, self.__var_value__, self.__job_uuid__)
    else:
      return 'bgapi hupall %s\nJob-UUID: %s\n\n' % (self.__cause__,
        self.__job_uuid__)

class KillCommand(UUIDCommand):
  '''
  Reset a specific <uuid> channel. 

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
              cause - reason for reset.
  '''
  def __init__(self, *args, **kwargs):
    super(KillCommand, self).__init__(*args, **kwargs)
    self.__cause__ = kwargs.get('cause')

  def get_cause(self):
    return self.__cause__

  def __str__(self):
    if not self.__cause__:
      return 'bgapi uuid_kill %s\nJob-UUID: %s\n\n' % (self.__uuid__,
        self.__job_uuid__)
    else:
      return 'bgapi uuid_kill %s %s\nJob-UUID: %s\n\n' % (self.__uuid__,
        self.__cause__, self.__job_uuid__)

class LimitCommand(UUIDCommand):
  '''
  Apply or change limit(s) on a specified uuid. 

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
              backend - The backend to use. 
              realm - Arbitrary name.
              resource - The resource on which to limit the number of calls. 
              max_calls - The maximum number of concurrent calls allowed to pass 
                          or a call rate in calls/sec. If not set or set to a negative 
                          value the limit application only acts as a counter.
              interval - calls per second.
              number - destination number
              dialplan - destination dialplan
              context - destination context
  '''
  def __init__(self, *args, **kwargs):
    super(LimitCommand, self).__init__(*args, **kwargs)
    self.__backend__ = kwargs.get('backend')
    self.__realm__ = kwargs.get('realm')
    self.__resource__ = kwargs.get('resource')
    self.__max_calls__ = kwargs.get('max_calls')
    self.__interval__ = kwargs.get('interval')
    self.__number__ = kwargs.get('number')
    self.__dialplan__ = kwargs.get('dialplan')
    self.__context__ = kwargs.get('context')

  def get_backend(self):
    return self.__backend__

  def get_realm(self):
    return self.__realm__

  def get_resource(self):
    return self.__resource__

  def get_max_calls(self):
    return self.__max_calls__

  def __str__(self):
    buffer = StringIO()
    buffer.write('bgapi uuid_limit %s %s %s %s' % (self.__uuid__,
      self.__backend__, self.__realm__, self.__resource__))
    if self.__max_calls__:
      buffer.write(' %i' % self.__max_calls__)
      if self.__interval__:
        buffer.write('/%i' % self.__interval__)
    if self.__number__:
      buffer.write(' %s' % self.__number__)
      if self.__dialplan__:
        buffer.write(' %s' % self.__dialplan__)
        if self.__context__:
          buffer.write(' %s' % self.__context__)
    buffer.write('\nJob-UUID: %s\n\n' % self.__job_uuid__)
    try:
      return buffer.getvalue()
    finally:
      buffer.close()

class LoadModuleCommand(BackgroundCommand):
  '''
  Load external module 

  Arguments: sender - The freepy actor sending this command.
             name - module name.
  '''  
  def __init__(self, *args, **kwargs):
    super(LoadModuleCommand, self).__init__(*args, **kwargs)
    self.__name__ = kwargs.get('name')

  def get_name(self):
    return self.__name__

  def __str__(self):
    return 'bgapi load %s\nJob-UUID: %s\n\n' % (self.__name__,
      self.__job_uuid__)

class MaskRecordingCommand(UUIDCommand):
  '''
  Mask the audio associated with the given UUID into a file.

  Arguments: sender - The freepy actor sending this command.
             uuid - universal unique identifier.
             path - The path where the recording should be stored.
  '''  

  def __init__(self, *args, **kwargs):
    super(MaskRecordingCommand, self).__init__(*args, **kwargs)
    self.__path__ = kwargs.get('path', None)
    if not self.__path__:
      raise ValueError('A valid path parameter must be specified.')

  def __str__(self):
    return 'bgapi uuid_record %s mask %s\nJob-UUID: %s\n\n' % (self.__uuid__, self.__path__, \
      self.__job_uuid__)

class OriginateCommand(BackgroundCommand):
  '''
  Originate a new call. 

  Arguments: sender - The freepy actor sending this command.
             url - URL you are calling.
             extension - call extension.
             app_name - *
             app_args - arguments to the app specified by app_name
             options - **
  
  * These are valid application names that can be used in this context :
    park, bridge, javascript/lua/perl, playback (remove mod_native_file), and many others. 
  ** The following are options that can be passed :
      group_confirm_key
      group_confirm_file
      forked_dial
      fail_on_single_reject
      ignore_early_media
      return_ring_ready
      originate_retries
      originate_retry_sleep_ms
      origination_caller_id_name
      origination_caller_id_number
      originate_timeout
      sip_auto_answer 
  '''  

  def __init__(self, *args, **kwargs):
    super(OriginateCommand, self).__init__(*args, **kwargs)
    self.__url__ = kwargs.get('url')
    self.__extension__ = kwargs.get('extension')
    self.__app_name__ = kwargs.get('app_name')
    self.__app_args__ = kwargs.get('app_args', [])
    if not isinstance(self.__app_args__, list):
      raise TypeError('The app_args parameter must be a list type.')
    self.__options__ = kwargs.get('options', [])
    if not isinstance(self.__options__, list):
      raise TypeError('The options parameter must be a list type.')
    if self.__extension__ and self.__app_name__:
      raise RuntimeError('An originate command can specify either an \
      extension or an app_name but not both.')

  def get_app_name(self):
    return self.__app_name__

  def get_app_args(self):
    return self.__app_args__

  def get_extension(self):
    return self.__extension__

  def get_options(self):
    return self.__options__

  def get_url(self):
    return self.__url__

  def __str__(self):
    buffer = StringIO()
    buffer.write('bgapi originate ')
    if self.__options__:
      buffer.write('{%s}' % ','.join(self.__options__))
    buffer.write('%s ' % self.__url__)
    if self.__extension__:
      buffer.write('%s' % self.__extension__)
    else:
      if self.__app_args__:
        buffer.write('\'&%s(%s)\'' % (self.__app_name__, ' '.join(self.__app_args__)))
      else:
        buffer.write('&%s()' % self.__app_name__)
    buffer.write('\nJob-UUID: %s\n\n' % self.__job_uuid__)
    try:
      return buffer.getvalue()
    finally:
      buffer.close()

class ParkCommand(UUIDCommand):
  '''
  Park call 

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
  '''
  def __init__(self, *args, **kwargs):
    super(ParkCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi uuid_park %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class PauseCommand(UUIDCommand):
  '''
  Pause <uuid> media 

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
  '''
  def __init__(self, *args, **kwargs):
    super(PauseCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi pause %s on\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class PauseSessionCreationCommand(BackgroundCommand):
  '''
  inbound or outbound may optionally be specified to pause just inbound or outbound 
  session creation, both paused if nothing specified. resume has similar behavior. 

  Arguments: sender - The freepy actor sending this command.
             direction - inbound or outbound or None paramater value.
  '''  

  def __init__(self, *args, **kwargs):
    super(PauseSessionCreationCommand, self).__init__(*args, **kwargs)
    self.__direction__ = kwargs.get('direction')

  def get_direction(self):
    return self.__direction__

  def __str__(self):
    if not self.__direction__:
      return 'bgapi fsctl pause\nJob-UUID: %s\n\n' % self.__job_uuid__
    else:
      return 'bgapi fsctl pause %s\nJob-UUID: %s\n\n' % (self.__direction__,
        self.__job_uuid__)

class PreAnswerCommand(UUIDCommand):
  '''
  Preanswer a channel. 

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
  '''
  def __init__(self, *args, **kwargs):
    super(PreAnswerCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi uuid_pre_answer %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class PreProcessCommand(UUIDCommand):
  '''
  Pre-process Channel 

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
  '''
  def __init__(self, *args, **kwargs):
    super(PreProcessCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi uuid_preprocess %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class ReceiveDTMFCommand(UUIDCommand):
  '''
  Receve DTMF digits to <uuid> set.

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
              digits - Use the character w for a .5 second delay and the character W for a 1 second delay.
              tone_duration - Default tone duration is 2000ms. 
  '''
  def __init__(self, *args, **kwargs):
    super(ReceiveDTMFCommand, self).__init__(*args, **kwargs)
    self.__digits__ = kwargs.get('digits')
    self.__duration__ = kwargs.get('tone_duration')

  def get_digits(self):
    return self.__digits__

  def get_tone_duration(self):
    return self.__duration__

  def __str__(self):
    if not self.__duration__:
      return 'bgapi uuid_recv_dtmf %s %s\nJob-UUID: %s\n\n' % (self.__uuid__,
        self.__digits__, self.__job_uuid__)
    else:
      return 'bgapi uuid_recv_dtmf %s %s@%s\nJob-UUID: %s\n\n' % (self.__uuid__,
        self.__digits__, self.__duration__, self.__job_uuid__)

class ReclaimMemoryCommand(BackgroundCommand):
  '''
  Reclaim Memory

  Arguments: sender - The freepy actor sending this command.
  '''  

  def __init__(self, *args, **kwargs):
    super(ReclaimMemoryCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi fsctl reclaim_mem\nJob-UUID: %s\n\n' % self.__job_uuid__

class RenegotiateMediaCommand(UUIDCommand):
  '''
  API command to tell a channel to send a re-invite with optional list of new codecs

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
              codec - audio/video codec.
  '''
  def __init__(self, *args, **kwargs):
    super(RenegotiateMediaCommand, self).__init__(*args, **kwargs)
    self.__codec__ = kwargs.get('codec')

  def get_codec(self):
    return self.__codec__

  def __str__(self):
    return 'bgapi uuid_media_reneg %s =%s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__codec__, self.__job_uuid__)

class ResumeSessionCreationCommand(BackgroundCommand):
  '''
  inbound or outbound may optionally be specified to resume just inbound or outbound session creation,
  both paused if nothing specified.

  Arguments: sender - The freepy actor sending this command.
             direction - inbound or outbound or None paramater value.
  '''  

  def __init__(self, *args, **kwargs):
    super(ResumeSessionCreationCommand, self).__init__(*args, **kwargs)
    self.__direction__ = kwargs.get('direction')

  def get_direction(self):
    return self.__direction__

  def __str__(self):
    if not self.__direction__:
      return 'bgapi fsctl resume\nJob-UUID: %s\n\n' % self.__job_uuid__
    else:
      return 'bgapi fsctl resume %s\nJob-UUID: %s\n\n' % (self.__direction__,
        self.__job_uuid__)

class SendDTMFCommand(UUIDCommand):
  '''
  Send DTMF digits to <uuid> set.

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
              digits - Use the character w for a .5 second delay and the character W for a 1 second delay.
              tone_duration - Default tone duration is 2000ms. 
  '''
  def __init__(self, *args, **kwargs):
    super(SendDTMFCommand, self).__init__(*args, **kwargs)
    self.__digits__ = kwargs.get('digits')
    self.__duration__ = kwargs.get('tone_duration')

  def get_digits(self):
    return self.__digits__

  def get_tone_duration(self):
    return self.__duration__

  def __str__(self):
    if not self.__duration__:
      return 'bgapi uuid_send_dtmf %s %s\nJob-UUID: %s\n\n' % (self.__uuid__,
        self.__digits__, self.__job_uuid__)
    else:
      return 'bgapi uuid_send_dtmf %s %s@%i\nJob-UUID: %s\n\n' % (self.__uuid__,
        self.__digits__, self.__duration__, self.__job_uuid__)

class SendInfoCommand(UUIDCommand):
  '''
  Send info to the endpoint.

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
  '''
  def __init__(self, *args, **kwargs):
    super(SendInfoCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi uuid_send_info %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class SetAudioLevelCommand(UUIDCommand):
  '''
  Adjust the audio levels on a channel or mute (read/write) via a media bug.

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
              level - is in the range from -4 to 4, 0 being the default value. 
  '''
  def __init__(self, *args, **kwargs):
    super(SetAudioLevelCommand, self).__init__(*args, **kwargs)
    self.__audio_level__ = kwargs.get('level')
    if not self.__audio_level__ or self.__audio_level__ < -4.0 or \
      self.__audio_level__ > 4.0:
      raise ValueError('The level value %s is invalid.' % self.__audio_level__)

  def get_level(self):
    return self.__audio_level__

  def __str__(self):
    return 'bgapi uuid_audio %s start write level %f\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__audio_level__, self.__job_uuid__)

class SetDefaultDTMFDurationCommand(BackgroundCommand):
  '''
  Sets the default_dtmf_duration switch parameter. The number is in clock ticks (CT) where 
  CT / 8 = ms. The default_dtmf_duration specifies the DTMF duration to use on 
  originated DTMF events or on events that are received without a duration specified. 
  This value can be increased or lowered. This value is lower-bounded by min_dtmf_duration 
  and upper-bounded by max_dtmf_duration.

  Arguments: sender - The freepy actor sending this command.
             duration - paramter value.
  '''  

  def __init__(self, *args, **kwargs):
    super(SetDefaultDTMFDurationCommand, self).__init__(*args, **kwargs)
    self.__duration__ = kwargs.get('duration')

  def get_duration(self):
    return self.__duration__

  def __str__(self):
    return 'bgapi fsctl default_dtmf_duration %i\nJob-UUID: %s\n\n' % (self.__duration__,
      self.__job_uuid__)

class SetGlobalVariableCommand(BackgroundCommand):
  '''
  Sets the value of a global variable. 

  Arguments: sender - The freepy actor sending this command.
             name - name of global variable
             value - value of global variable
  '''  

  def __init__(self, *args, **kwargs):
    super(SetGlobalVariableCommand, self).__init__(*args, **kwargs)
    self.__name__ = kwargs.get('name')
    self.__value__ = kwargs.get('value')
    if not self.__name__ or not self.__value__:
      raise RuntimeError('The set global variable command requires both name \
      and value parameters.')

  def get_name(self):
    return self.__name__

  def get_value(self):
    return self.__value__

  def __str__(self):
    return 'bgapi global_setvar %s=%s\nJob-UUID: %s\n\n' % (self.__name__,
      self.__value__, self.__job_uuid__)

class SetMaximumDTMFDurationCommand(BackgroundCommand):
  '''
  Sets the max_dtmf_duration switch parameter. The number is in clock ticks (CT) where CT / 8 = ms. 
  The max_dtmf_duration caps the playout of a DTMF event at the specified duration. 
  Events exceeding this duration will be truncated to this duration. 
  You cannot configure a duration on a profile that exceeds this setting. 
  This setting can be lowered, but cannot exceed 192000 (the default). 
  This setting cannot be set lower than min_dtmf_duration.

  Arguments: sender - The freepy actor sending this command.
             duration - the maximum duration if a DTMF event. 
  '''  

  def __init__(self, *args, **kwargs):
    super(SetMaximumDTMFDurationCommand, self).__init__(*args, **kwargs)
    self.__duration__ = kwargs.get('duration')

  def get_duration(self):
    return self.__duration__

  def __str__(self):
    return 'bgapi fsctl max_dtmf_duration %i\nJob-UUID: %s\n\n' % (self.__duration__,
      self.__job_uuid__)

class SetMinimumDTMFDurationCommand(BackgroundCommand):
  '''
  Sets the min_dtmf_duration switch parameter to 100ms. The number is in clock ticks where clockticks / 8 = ms. 
  The min_dtmf_duration specifies the minimum DTMF duration to use on outgoing events. 
  Events shorter than this will be increased in duration to match min_dtmf_duration. 
  You cannot configure a DTMF duration on a profile that is less than this setting. 
  You may increase this value, but cannot set it lower than 400 (the default). 
  This value cannot exceed max_dtmf_duration.

  Arguments: sender - The freepy actor sending this command.
             duration - value of parameter.
  '''  

  def __init__(self, *args, **kwargs):
    super(SetMinimumDTMFDurationCommand, self).__init__(*args, **kwargs)
    self.__duration__ = kwargs.get('duration')

  def get_duration(self):
    return self.__duration__

  def __str__(self):
    return 'bgapi fsctl min_dtmf_duration %i\nJob-UUID: %s\n\n' % (self.__duration__,
      self.__job_uuid__)

class SetMultipleVariableCommand(UUIDCommand):
  '''
  Set multiple vars on a channel. 

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
              variables - a dictionary list of key/value pairs to set.
  '''
  def __init__(self, *args, **kwargs):
    super(SetMultipleVariableCommand, self).__init__(*args, **kwargs)
    self.__variables__ = kwargs.get('variables')
    if not isinstance(self.__variables__, dict):
      raise TypeError('The variables parameter must be of type dict.')
    variable_list = list()
    for key, value in self.__variables__.iteritems():
      variable_list.append('%s=%s' % (key, value))
    self.__variables_string__ = ';'.join(variable_list)

  def __str__(self):
    return 'bgapi uuid_setvar_multi %s %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__variables_string__, self.__job_uuid__)

class SetSessionsPerSecondCommand(BackgroundCommand):
  '''
  This changes the sessions-per-second limit as initially set in switch.conf 

  Arguments: sender - The freepy actor sending this command.
             sessions_per_second - value for paramater.
  '''  

  def __init__(self, *args, **kwargs):
    super(SetSessionsPerSecondCommand, self).__init__(*args, **kwargs)
    self.__sessions_per_second__ = kwargs.get('sessions_per_second')

  def get_sessions_per_second(self):
    return self.__sessions_per_second__

  def __str__(self):
    return 'bgapi fsctl sps %i\nJob-UUID: %s\n\n' % (self.__sessions_per_second__,
      self.__job_uuid__)

class SetVariableCommand(UUIDCommand):
  '''
  Set a variable on a channel.

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
              name - name of the variable.
              value - value of the variable.
  '''
  def __init__(self, *args, **kwargs):
    super(SetVariableCommand, self).__init__(*args, **kwargs)
    self.__name__ = kwargs.get('name')
    self.__value__ = kwargs.get('value')
    if not self.__name__ or not self.__value__:
      raise RuntimeError('The set variable command requires both name \
      and value parameters.')

  def get_name(self):
    return self.__name__

  def get_value(self):
    return self.__value__

  def __str__(self):
    return 'bgapi uuid_setvar %s %s %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__name__, self.__value__, self.__job_uuid__)

class ShutdownCommand(BackgroundCommand):
  '''
  Stop the FreeSWITCH program. 

  Arguments: sender - The freepy actor sending this command.
             option - paramater value [cancel, elegant, asap, restart]*
             
  * available options: 
    cancel - discontinue a previous shutdown request.
    elegant - wait for all traffic to stop; do not prevent new traffic.
    asap - wait for all traffic to stop; do not allow new traffic.
    restart - restart FreeSWITCH immediately following the shutdown. 
  '''  

  def __init__(self, *args, **kwargs):
    super(ShutdownCommand, self).__init__(*args, **kwargs)
    self.__option__ = kwargs.get('option')
    if self.__option__ and not self.__option__ == 'cancel' and \
      not self.__option__ == 'elegant' and not self.__option__ == 'asap' and \
      not self.__option__ == 'restart':
      raise ValueError('The option %s is an invalid option.' % self.__option__)

  def get_option(self):
    return self.__option__

  def __str__(self):
    if not self.__option__:
      return 'bgapi fsctl shutdown\nJob-UUID: %s\n\n' % self.__job_uuid__
    else:
      return 'bgapi fsctl shutdown %s\nJob-UUID: %s\n\n' % (self.__option__,
        self.__job_uuid__)

class SimplifyCommand(UUIDCommand):
  '''
  This command directs FreeSWITCH to remove itself from the SIP signaling path if it can safely do so 

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
  '''
  def __init__(self, *args, **kwargs):
    super(SimplifyCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi uuid_simplify %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class StartDebugMediaCommand(UUIDCommand):
  '''
  Start the Debug Media.

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
              option - [read|write|both|vread|vwrite|vboth]
  '''
  def __init__(self, *args, **kwargs):
    super(StartDebugMediaCommand, self).__init__(*args, **kwargs)
    self.__option__ = kwargs.get('option')

  def get_option(self):
    return self.__option__

  def __str__(self):
    return 'bgapi uuid_debug_media %s %s on\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__option__, self.__job_uuid__)

class StartDisplaceCommand(UUIDCommand):
  '''
  Displace the audio for the target <uuid> with the specified audio <path>. 

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
              path - path to an audio source (wav, shout, etc...) 
              limit - number of seconds before terminating the displacement
              mux - cause the original audio to be mixed together with 'file', 
              i.e. you can still converse with the other party while the file is playing
  '''
  def __init__(self, *args, **kwargs):
    super(StartDisplaceCommand, self).__init__(*args, **kwargs)
    self.__path__ = kwargs.get('path')
    self.__limit__ = kwargs.get('limit')
    self.__mux__ = kwargs.get('mux')

  def get_limit(self):
    return self.__limit__

  def get_mux(self):
    return self.__mux__

  def get_path(self):
    return self.__path__

  def __str__(self):
    buffer = StringIO()
    buffer.write('bgapi uuid_displace %s start %s' % (self.__uuid__,
      self.__path__))
    if self.__limit__:
      buffer.write(' %i' % self.__limit__)
    if self.__mux__:
      buffer.write(' mux')
    buffer.write('\nJob-UUID: %s\n\n' % self.__job_uuid__)
    try:
      return buffer.getvalue()
    finally:
      buffer.close()

class StartRecordingCommand(UUIDCommand):
  '''
  Record the audio associated with the given UUID into a file.

  Arguments: sender - The freepy actor sending this command.
             uuid - universal unique identifier.
             path - The path where the recording should be stored.
             max_length - The max recording length in seconds.
  '''  

  def __init__(self, *args, **kwargs):
    super(StartRecordingCommand, self).__init__(*args, **kwargs)
    self.__path__ = kwargs.get('path', None)
    self.__max_length__ = kwargs.get('max_length', None)
    if not self.__path__:
      raise ValueError('A valid path parameter must be specified.')

  def __str__(self):
    if self.__max_length__:
      return 'bgapi uuid_record %s start %s %i\nJob-UUID: %s\n\n' % (self.__uuid__, self.__path__, \
        self.__max_length__, self.__job_uuid__)
    else:  
      return 'bgapi uuid_record %s start %s\nJob-UUID: %s\n\n' % (self.__uuid__, self.__path__, \
        self.__job_uuid__)

class StatusCommand(BackgroundCommand):
  '''
  Show current status 

  Arguments: sender - The freepy actor sending this command.
  '''  
  def __init__(self, *args, **kwargs):
    super(StatusCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi status\nJob-UUID: %s\n\n' % self.__job_uuid__

class StopDebugMediaCommand(UUIDCommand):
  '''
  Used to stop the debug media.

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
  '''
  def __init__(self, *args, **kwargs):
    super(StopDebugMediaCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi uuid_debug_media %s off\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class StopDisplaceCommand(UUIDCommand):
  '''
  Stop displacing the audio for the target <uuid>

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
  '''
  def __init__(self, *args, **kwargs):
    super(StopDisplaceCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi uuid_displace %s stop\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class StopRecordingCommand(UUIDCommand):
  '''
  Stop recording the audio associated with the given UUID into a file.

  Arguments: sender - The freepy actor sending this command.
             uuid - universal unique identifier.
             path - The path where the recording should be stored.
  '''  

  def __init__(self, *args, **kwargs):
    super(StopRecordingCommand, self).__init__(*args, **kwargs)
    self.__path__ = kwargs.get('path', None)
    if not self.__path__:
      raise ValueError('A valid path parameter must be specified.')

  def __str__(self):
    return 'bgapi uuid_record %s stop %s\nJob-UUID: %s\n\n' % (self.__uuid__, self.__path__, \
      self.__job_uuid__)

class SyncClockCommand(BackgroundCommand):
  '''
  FreeSWITCH will not trust the system time. It gets one sample of system time when it first starts and 
  uses the monotonic clock from there. You can sync it back to real time with "fsctl sync_clock"
  Note: 'fsctl sync_clock' immediately takes effect - which can affect the times on your CDRs. 
  You can end up undrebilling/overbilling, or even calls hungup before they originated. 
  e.g. if FS clock is off by 1 month, then your CDRs are going to show calls that lasted for 1 month!
  'fsctl sync_clock_when_idle' is much safer, which does the same sync but doesn't take effect until 
  there are 0 channels in use. That way it doesn't affect any CDRs. 

  Arguments: sender - The freepy actor sending this command.
  '''  

  def __init__(self, *args, **kwargs):
    super(SyncClockCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi fsctl sync_clock\nJob-UUID: %s\n\n' % self.__job_uuid__

class SyncClockWhenIdleCommand(BackgroundCommand):
  '''
  You can sync the clock but have it not do it till there are 0 calls (r:2094f2d3) 

  Arguments: sender - The freepy actor sending this command.
  '''  
  def __init__(self, *args, **kwargs):
    super(SyncClockWhenIdleCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi fsctl sync_clock_when_idle\nJob-UUID: %s\n\n' % self.__job_uuid__

class TransferCommand(UUIDCommand):
  '''
  Transfers an existing call to a specific extension within a <dialplan> and <context>.

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
              leg - bleg or both.
              extension - destination extension.  
              dialplan - destination dialplan.*   
              context - destination context.
  * Dialplan may be "xml" or "directory".
  '''
  def __init__(self, *args, **kwargs):
    super(TransferCommand, self).__init__(*args, **kwargs)
    self.__leg__ = kwargs.get('leg')
    self.__extension__ = kwargs.get('extension')
    self.__dialplan__ = kwargs.get('dialplan')
    self.__context__ = kwargs.get('context')

  def get_context(self):
    return self.__context__

  def get_dialplan(self):
    return self.__dialplan__

  def get_extension(self):
    return self.__extension__

  def get_leg(self):
    return self.__leg__

  def __str__(self):
    buffer = StringIO()
    buffer.write('bgapi uuid_transfer %s' % self.__uuid__)
    if self.__leg__:
      buffer.write(' %s' % self.__leg__)
    buffer.write(' %s' % self.__extension__)
    if self.__dialplan__:
      buffer.write(' %s' % self.__dialplan__)
    if self.__context__:
      buffer.write(' %s' % self.__context__)
    buffer.write('\nJob-UUID: %s\n\n' % self.__job_uuid__)
    try:
      return buffer.getvalue()
    finally:
      buffer.close()

class UnholdCommand(UUIDCommand):
  '''
  Take a call off hold.

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
  '''
  def __init__(self, *args, **kwargs):
    super(UnholdCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi uuid_hold off %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class UnloadModuleCommand(BackgroundCommand):
  '''
  Unload external module. 

  Arguments: sender - The freepy actor sending this command.
             name - name of external module to unload.
             force - force unload. Default set to False.
  '''  

  def __init__(self, *args, **kwargs):
    super(UnloadModuleCommand, self).__init__(*args, **kwargs)
    self.__name__ = kwargs.get('name')
    self.__force__ = kwargs.get('force', False)

  def get_name(self):
    return self.__name__

  def get_force(self):
    return self.__force__

  def __str__(self):
    if not self.__force__:
      return 'bgapi unload %s\nJob-UUID: %s\n\n' % (self.__name__,
        self.__job_uuid__)
    else:
      return 'bgapi unload -f %s\nJob-UUID: %s\n\n' % (self.__name__,
        self.__job_uuid__)

class UnmaskRecordingCommand(UUIDCommand):
  '''
  Unmask the audio associated with the given UUID into a file.

  Arguments: sender - The freepy actor sending this command.
             uuid - universal unique identifier.
             path - The path where the recording should be stored.
  '''  

  def __init__(self, *args, **kwargs):
    super(UnmaskRecordingCommand, self).__init__(*args, **kwargs)
    self.__path__ = kwargs.get('path', None)
    if not self.__path__:
      raise ValueError('A valid path parameter must be specified.')

  def __str__(self):
    return 'bgapi uuid_record %s unmask %s\nJob-UUID: %s\n\n' % (self.__uuid__, self.__path__, \
      self.__job_uuid__)

class UnpauseCommand(UUIDCommand):
  '''
  UnPause <uuid> media.

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
  '''
  def __init__(self, *args, **kwargs):
    super(UnpauseCommand, self).__init__(*args, **kwargs)

  def __str__(self):
    return 'bgapi pause %s off\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__job_uuid__)

class UnsetVariableCommand(UUIDCommand):
  '''
  UnSet a variable on a channel. 

  Arguments:  sender - The freepy actor sending this command.
              uuid - universal unique identifier.
              name - variable to be unset.
  '''
  def __init__(self, *args, **kwargs):
    super(UnsetVariableCommand, self).__init__(*args, **kwargs)
    self.__name__ = kwargs.get('name')
    if not self.__name__:
      raise RuntimeError('The unset variable commands requires the name \
      parameter.')

  def get_name(self):
    return self.__name__

  def __str__(self):
    return 'bgapi uuid_setvar %s %s\nJob-UUID: %s\n\n' % (self.__uuid__,
      self.__name__, self.__job_uuid__)
