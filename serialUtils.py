# coding: utf-8

"""serialUtils.py: Python serial port utils"""

__author__ = "David Leval"
__copyright__ = "Copyright 2020, DLE-Dev"
__license__ = "GPL"
__version__ = "1.1"
__email__ = "dleval@dle-dev.com"

import sys
import glob
import serial

def list_serial_ports():
    """ 
    Lists serial port names
    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def listUSBSerialPorts():
    """ 
    Lists  USB serial port available on the system
    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        USB serial ports list with VID, PID, Serial ...
    """
    if sys.platform.startswith('win'):
        import serial.tools.list_ports
        ports = list(serial.tools.list_ports.comports())
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        import serial.tools.list_ports_linux
        ports = list(serial.tools.list_ports_linux.comports())
    elif sys.platform.startswith('darwin'):
        import serial.tools.list_ports_osx
        ports = list(serial.tools.list_ports_osx.comports())
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port_no, description, address in ports:
        if 'USB' in address:
            result.append([port_no, description, address])
    return result


def USBSerialFind(*args):
    """ 
    Search for USB serial device with information (PID, VID, Serial, Description ...)
    :raises SystemError:
        (No USB serial device detected) or
        (No USB serial device with all args detected)
    :returns:
         Port corresponding to the serial USB device
    """
    port_ret = []
    serialPortsAvailable = listUSBSerialPorts()
    if bool(serialPortsAvailable):
        for port in serialPortsAvailable:
            port_no, description, address = port
            if all(x in (description + address) for x in [*args]):
                # print("Find Device:", description)
                port_ret.append(port_no)
        if not port_ret:
            raise SystemError(f"No USB serial device with {args} detected")
        return port_ret
    else:
        raise SystemError('No USB serial device detected')


def connectUSBSerialFind(*args, baudrate):
    devicePort = USBSerialFind(*args)
    deviceCom = serial.Serial(devicePort[0], baudrate, timeout=2)
    print("Open USB serial port :", devicePort[0])
    return deviceCom
