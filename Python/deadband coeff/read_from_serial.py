'''
Experiment: Dead Band Entry Testing 
By: Jia Bhargava, Tanay Srinivasa
Last Modified: 24 June 2024

Run bi_steer_cycle_testing arduino code with deadband_test()
'''

import serial
import time
import os
import csv
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

# FRONT_PATH = './Python/dead band slope/SourceData4095/FrontSlope40Data_1.csv'
# REAR_PATH = './Python/dead band slope/SourceData4095/RearSlope40Data.csv'
# FRONT_COMP_PATH = './Python/dead band slope/SourceData4095/FrontCompensatedData.csv'
# REAR_COMP_PATH = './Python/dead band slope/SourceData4095/RearCompensatedData.csv'
COM = '/dev/cu.usbmodem160464801'
BAUD = 115200

# Function to Read Accelerometer, Complimentary Filter, Kalman Filter Angles #
def read_from_serial(path):
    # Adding Header Row with Columns of CSV #
    with open(path, mode='w') as sensor_file:
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
            with open(path, mode='a') as sensor_file:
                line = data.split(',')
                sensor_writer = csv.writer(
                        sensor_file, 
                        delimiter=',', 
                        quotechar='"', 
                        quoting=csv.QUOTE_MINIMAL
                        )
                sensor_writer.writerow([line[0],line[1],line[2],line[3]])

def read_front_and_rear(front_path, rear_path,overwrite=False):
    if overwrite == False and (os.path.exists(front_path) or os.path.exists(rear_path)):
        print('File Already Exists, Try Again')
        return

    # Adding Header Row with Columns of CSV #
    with open(front_path, mode='w') as front_file:
        front_writer = csv.writer(
                front_file, 
                delimiter=',', 
                quotechar='"', 
                quoting=csv.QUOTE_MINIMAL
                )
        front_writer.writerow(['Time','Wheel Input','Wheel Ticks','Wheel Speed'])
    
    with open(rear_path, mode='w') as rear_file:
        rear_writer = csv.writer(
                rear_file, 
                delimiter=',', 
                quotechar='"', 
                quoting=csv.QUOTE_MINIMAL
                )
        rear_writer.writerow(['Time','Wheel Input','Wheel Ticks','Wheel Speed'])
    
    # Creating Serial Object for COM Port and Selected Baud Rate #
    x = serial.Serial(COM, BAUD, timeout=0.1)

    # Reading Serial Values and Storing into CSV #
    while x.isOpen() is True:
        data = x.readline().decode('utf-8')
        print(data)
        data = str(x.readline().decode('utf-8')).rstrip()
        if data != '':
            with open(front_path, mode='a') as sensor_file:
                line = data.split(',')
                sensor_writer = csv.writer(
                        sensor_file, 
                        delimiter=',', 
                        quotechar='"', 
                        quoting=csv.QUOTE_MINIMAL
                        )
                sensor_writer.writerow([line[0],line[1],line[2],line[3]])
            
            with open(rear_path, mode='a') as sensor_file:
                line = data.split(',')
                sensor_writer = csv.writer(
                        sensor_file, 
                        delimiter=',', 
                        quotechar='"', 
                        quoting=csv.QUOTE_MINIMAL
                        )
                sensor_writer.writerow([line[0],line[1],line[4],line[5]])

def sign(num):
    if num > 0:
        return 1
    return -1

def read_and_store_constants(path):
    # Adding Header Row with Columns of CSV #
    with open(path, mode='w') as sensor_file:
        sensor_writer = csv.writer(
                sensor_file, 
                delimiter=',', 
                quotechar='"', 
                quoting=csv.QUOTE_MINIMAL
                )
        sensor_writer.writerow(['Time','Wheel Input','Wheel Ticks','Wheel Speed'])
    
    # Creating Serial Object for COM Port and Selected Baud Rate #
    x = serial.Serial(COM, BAUD, timeout=0.1)

    zero_crosses = 0
    prev_sign = 1
    # Reading Serial Values and Storing into CSV #
    while x.isOpen() is True:
        data = x.readline().decode('utf-8')
        print(data)
        data = str(x.readline().decode('utf-8')).rstrip()
        if data != '':
            with open(path, mode='a') as sensor_file:
                line = data.split(',')
                sensor_writer = csv.writer(
                        sensor_file, 
                        delimiter=',', 
                        quotechar='"', 
                        quoting=csv.QUOTE_MINIMAL
                        )
                sensor_writer.writerow([line[0],line[1],line[2],line[3]])
            
            if sign(int(line[1])) != prev_sign:
                zero_crosses += 1
                prev_sign = sign(int(line[1]))
        
        if zero_crosses == 21:
            break
    
    print('Completed 10 Time Periods')

def plot_raw(path):
    df = pd.read_csv(path)
    df['Relative Time'] = df['Time']-df['Time'].iloc[0]

    plt.subplot(2,1,1)
    plt.plot(df['Relative Time'],df['Wheel Input'])
    plt.subplot(2,1,2)
    plt.plot(df['Relative Time'],df['Wheel Speed'])
    plt.show()

if __name__ == '__main__':
    front_path = './Python/deadband coeff/SourceData10/FrontSlope15Data.csv'
    rear_path = './Python/deadband coeff/SourceData10/RearSlope15Data.csv'
    read_front_and_rear(front_path,rear_path)
    plot_raw(front_path)
    plot_raw(rear_path)
    
    # read_from_serial(path)
    # plot_raw(path)
    # path = './Python/deadband coeff/tmp.csv'
    # read_and_store_constants(path)
