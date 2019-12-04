import serial
import pandas as pd
#import matplotlib.pyplot as plt
import numpy as np
from time import sleep
from dataclasses import dataclass
import serial.tools.list_ports
import json

def open_serial_connection(serial_port = "COM1", baud_rate = 9600):
   return serial.Serial(serial_port, 9600)

def record_serial_data(serial_connection,  number_of_lines):
   data =[]
   serial_connection.flushInput()
   for i in range(number_of_lines):
      line = serial_connection.readline().decode('UTF-8')
      if(line.startswith("API")):
         print(line)
         data.append(line )    
   return data

def continous_record_serial_data(serial_connection, print_to_console = False, flush= True):
   data =[]

   if flush:
      serial_connection.flushInput()
   sleep(0.1)
   try:
      while True:
         line = serial_connection.readline().decode('UTF-8')
         print(line)
         if(line.startswith("API")):
            if print_to_console:
               print(line)
            data.append(line )    
   except:
      pass
      return data


def extract_color_from_line(line):
   split_line = line.split(",")
   if(split_line[1] =="COLOR"):
      return {'red':float(split_line[2] ),'green':float(split_line[3] ),'blue':float(split_line[4] )}
   else:
      return {}

def extract_float_from_line(line):
   split_line = line.split(",")
   if(split_line[1] =="FLOAT"):
      return {'value':float(split_line[2] )}
   else:
      return {}


def extract_color4_from_line(line):
   split_line = line.split(",")
   if(split_line[1] =="COLOR4"):
      return {'red':float(split_line[2] ),'green':float(split_line[3] ),'blue':float(split_line[4] ),'brightness':float(split_line[5] )}
   else:
      return {}


def extract_message_from_line(line):
   split_line = line.split(",")
   if(split_line[1] =="MESSAGE"):
      return {'MESSAGE':split_line[2]}
   else:
      return {}

def extract_from_serial_lines(serial_lines, extract_funtion):
   data = []
   for line in serial_lines:
      data.append(extract_funtion(line))
   return pd.DataFrame(data)

class Message:
   # def __init__(self, serial_device_name):
   #    self.m_message = "#,{}".format(serial_device_name)

   # def append(self, message_string):
   #    self.m_message += ",{}".format(message_string)

   # def hand_over(self):
   #    self.m_message += "\n"
   #    return str.encode(self.m_message)
   
   def __init__(self,serial_device_name ):
      self.m_message = {"dev":serial_device_name,'data':{}}

   def append(self, key, value):
      self.m_message['data'][key] = value

   def hand_over(self):
      return str.encode("#{}\n".format(self.m_message))

class SerialArduino:
   def __init__(self, serial_device_name, baud_rate):
      self.m_serial_connection = serial.Serial(serial_device_name, baud_rate) 
      self.m_serial_device_name = serial_device_name 

   def write(self, message_body):
      message = Message(self.m_serial_device_name)
      message.append("message",message_body)
      self.m_serial_connection.write(message.hand_over())

   def write_message(self, message):
      self.m_serial_connection.write(message.hand_over())

   def read_line(self):
      return self.m_serial_connection.readline()

   def close(self):
      self.m_serial_connection.close()

