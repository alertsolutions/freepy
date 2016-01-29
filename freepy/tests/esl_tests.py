from nose.tools import *
from mock import Mock, patch
from freepy.lib.esl import EventSocketClient, IEventSocketClientObserver


class TestObserver(IEventSocketClientObserver):
    def __init__(self):
        super(TestObserver, self).__init__()
        self.events = []

    def on_event(self, event):
        self.events.append(event)


class TestEventClientSocket(object):
    heartbeat = """Content-Length: 882
Content-Type: text/event-plain

Event-Name: HEARTBEAT
Core-UUID: 3fd79e98-4a01-4322-b514-6c9948a853b4
FreeSWITCH-Hostname: atjswitch
FreeSWITCH-Switchname: atjswitch
FreeSWITCH-IPv4: 172.25.10.40
FreeSWITCH-IPv6: %3A%3A1
Event-Date-Local: 2015-10-02%2015%3A40%3A09
Event-Date-GMT: Fri,%2002%20Oct%202015%2019%3A40%3A09%20GMT
Event-Date-Timestamp: 1443814809447596
Event-Calling-File: switch_core.c
Event-Calling-Function: send_heartbeat
Event-Calling-Line-Number: 73
Event-Sequence: 929
Event-Info: System%20Ready
Up-Time: 0%20years,%200%20days,%201%20hour,%203%20minutes,%2040%20seconds,%2094%20milliseconds,%20656%20microseconds
FreeSWITCH-Version: 1.4.20%2Bgit~20150703T164215Z~b95362f965~64bit
Uptime-msec: 3820094
Session-Count: 0
Max-Sessions: 1000
Session-Per-Sec: 1
Session-Per-Sec-Max: 1
Session-Per-Sec-FiveMin: 0
Session-Since-Startup: 0
Session-Peak-Max: 0
Session-Peak-FiveMin: 0
Idle-CPU: 98.633333

"""

    def get_esl(self):
        tob = TestObserver()
        esl = EventSocketClient(tob)
        esl.transport = Mock()
        esl.transport.getPeer.return_value = Mock(host='localhost', port=8021)
        esl.connectionMade()
        return (tob, esl)

    def test_dataReceived(self):
        tob, esl = self.get_esl()
        esl.dataReceived(self.heartbeat)
        assert_equal('send_heartbeat',
                     tob.events[0].get_header('Event-Calling-Function'))

    def test_dataReceived_buffer_ends_before_colon(self):
        tob, esl = self.get_esl()
        esl.dataReceived("""Content-Length: 19
Content-Type: text/event-plain

Header: Value
Broken""")
        print tob.events[0]
        print tob.events[0].get_headers()
        assert_equal('Value', tob.events[0].get_header('Header'))
        assert_is_none(tob.events[0].get_header('Broken'))
