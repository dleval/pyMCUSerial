# pyMCUSerial
Serial communication tools between a python program and a microncrolleur

## Example of usage

```python
import serial
from serialUtils import listUSBSerialPorts, connectUSBSerialFind

deviceCom = serial.Serial()

try:
  deviceCom = connectUSBSerialFind("0403:6015", baudrate=57600) #Replace with the VID:PID of your serial USB device
except SystemError as err:
  print("System error: {0}".format(err))
  print("List USB serial port available :")
  print(listUSBSerialPorts())
  
if(deviceCom.is_open == True):
  print("Serial port successfully connected")
  deviceCom.close()

```
