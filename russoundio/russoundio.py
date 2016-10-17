"""
Russound I/O interface

Copyright (c) 2016 Neil Lathwood <https://github.com/laf/ http://www.lathwood.co.uk/>

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.  Please see LICENSE.txt at the top level of
the source code distribution for details.

"""

import logging
import sys
import time
import socket

_LOGGER = logging.getLogger(__name__)

class RussoundIO:

    def __init__(self, host, port):
        """ Initialise RussoundIO class """

        self._host = host
        self._port = int(port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, keypad):
        """ Connect to the tcp gateway """

        try:
            self.sock.connect((self._host, self._port))
            self._keypad = keypad
        except socket.error as msg:
            _LOGGER.error(msg)
            return False

    def is_connected(self):
        """ Check we are connected """

        try:
            if self.sock.getpeername():
                return True
            else:
                return False
        except:
            return False

    def set_power(self, controller, zone, power):
        """ Switch power on/off to a zone """

        if power == '0':
            cmd = 'ZoneOff'
        elif power == '1':
            cmd = 'ZoneOn'

        self.send_cmd(controller, zone, cmd)

    def set_volume(self, controller, zone, volume):
        """ Set volume for zone to specific value """

    def set_source(self, controller, zone, source):
        """ Set source for a zone """

    def all_on_off(self):
        """ Turn all zones on or off """

    def toggle_mute(self, controller, zone):
        """ Toggle mute on/off for a zone """

    def get_power(self, controller, zone):
        """ Get source power status """

    def send_cmd(self, controller, zone, cmd, data=''):
        """ Send data to connected gateway """

        event = "C[%s].Z[%s]!%s %s" % (controller, zone, cmd, data)
        self.sock.send(event.encode())

    def receive_data(self, timeout=2):
        """ Receive data from connected gateway """

        self.sock.setblocking(0)
     
        #total data partwise in an array
        total_data=[];
        data='';
     
        #beginning time
        begin=time.time()
        while 1:
            #if you got some data, then break after timeout
            if total_data and time.time()-begin > timeout:
                break
         
            #if you got no data at all, wait a little longer, twice the timeout
            elif time.time()-begin > timeout*2:
                break
         
            #recv something
            try:
                data = self.sock.recv(8192)
                if data:
                    total_data.append(data)
                    #change the beginning time for measurement
                    begin=time.time()
                else:
                    #sleep for sometime to indicate a gap
                    time.sleep(0.1)
            except:
                pass
     
        #join all parts to make final string
        return b''.join(total_data)

    def __exit__(self):
        """ Close connection to gateway """
        try:
            self.sock.close()
        except socket.error as msg:
            print("Couldn't disconnect")
