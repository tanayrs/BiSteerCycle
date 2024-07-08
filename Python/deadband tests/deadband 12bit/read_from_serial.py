'''
Experiment: Dead Band Testing
By: Jia Bhargava, Tanay Srinivasa
Last Modified: 24 June 2024

Run bi_steer_cycle_testing arduino code with deadband_testing()
'''

import serial
import time
import csv
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

FRONT_PATH = './Python/dead band slope/SourceData4095/FrontUncompensatedData_1.csv'
REAR_PATH = './Python/dead band slope/SourceData4095/RearUncompensatedData.csv'
FRONT_COMP_PATH = './Python/dead band slope/SourceData4095/FrontCompensatedData.csv'
REAR_COMP_PATH = './Python/dead band slope/SourceData4095/RearCompensatedData.csv'
COM = '/dev/cu.usbmodem160464801'
BAUD = 115200

def read_from_serial():
    # Adding Header Row with Columns of CSV #
    with open(FRONT_PATH, mode='w') as sensor_file:
        sensor_writer = csv.writer(
                sensor_file, 
                delimiter=',', 
                quotechar='"', 
                quoting=csv.QUOTE_MINIMAL
                )
        sensor_writer.writerow(['Time','Wheel Input','Wheel Ticks','Wheel Speed'])
    
    # Creating Serial Object for COM Port and Selected Baud Rate #
    x = serial.Serial(COM, BAUD, timeout=0.1)

    # Reading Serial Values and Storing into CSV #
    while x.isOpen() is True:
        data = x.readline().decode('utf-8')
        print(data)
        data = str(x.readline().decode('utf-8')).rstrip()
        if data != '':
            with open(FRONT_PATH, mode='a') as sensor_file:
                line = data.split(',')
                sensor_writer = csv.writer(
                        sensor_file, 
                        delimiter=',', 
                        quotechar='"', 
                        quoting=csv.QUOTE_MINIMAL
                        )
                sensor_writer.writerow([line[0],line[1],line[2],line[3]])

if __name__ == '__main__':
    read_from_serial()