'''
Experiment: Dead Band Entry Testing 
By: Jia Bhargava, Tanay Srinivasa

Run bi_steer_cycle_testing arduino code with deadband_test()
'''

import serial
import os
import csv
from matplotlib import pyplot as plt
import pandas as pd

COM = '/dev/cu.usbmodem160464801'
BAUD = 115200

def sign(num):
    if num > 0:
        return 1
    return -1

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

    zero_crosses = 0
    prev_sign = 1

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
            
            if sign(int(line[1])) != prev_sign:
                zero_crosses += 1
                prev_sign = sign(int(line[1]))
        
        if zero_crosses == 21:
            break
    
    print('Completed 10 Time Periods')

def calculate_expected_output(pwm):
    PWM_RESOLUTION = 4095
    MOTOR_RPM = 587
    ratio = pwm/PWM_RESOLUTION
    expected_speed = (MOTOR_RPM/60)* ratio * 360
    return expected_speed

def plot_raw(path):
    df = pd.read_csv(path)
    df['Relative Time'] = df['Time']-df['Time'].iloc[0]
    df['Ideal Response'] = df['Wheel Input'].apply(calculate_expected_output)
    plt.subplot(2,1,1)
    plt.plot(df['Relative Time'],df['Wheel Input'])
    plt.subplot(2,1,2)
    
    plt.plot(df['Relative Time'],df['Wheel Speed'])
    plt.plot(df['Relative Time'],df['Ideal Response'], color='gray')
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    plt.show()

if __name__ == '__main__':
    front_path = './Python/deadband tests/deadband loaded/SourceData/FrontSlope10CompData.csv'
    rear_path = './Python/deadband tests/deadband loaded/SourceData/RearSlope10CompData.csv'
    read_front_and_rear(front_path,rear_path)
    plot_raw(front_path)
    plot_raw(rear_path)
    
    # read_from_serial(path)
    # plot_raw(path)
