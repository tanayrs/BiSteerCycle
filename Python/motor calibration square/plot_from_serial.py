'''
Experiment: Motor Calibration Testing with Square Input 
By: Jia Bhargava, Tanay Srinivasa
Last Modified: 13 June 2024

Run bi_steer_cycle arduino code with motor_calibration_square()
'''

import serial
import time
import csv
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

REAR_PATH = './Python/motor calibration square/SourceData/RearMotorCalibrationSquare150.csv'
FRONT_PATH = './Python/motor calibration square/SourceData/FrontMotorCalibrationSquare150.csv'

COM = '/dev/cu.usbmodem160464801'
BAUD = 115200

# Plotting Sensor Value Readings #
def plot_from_csv_rear():
    # Reading CSV into pandas DataFrame #
    df = pd.read_csv(REAR_PATH)

    # Printing Statistics of DataFrame #
    positive_df = df[df['Rear Wheel Input']>0]
    positive_mean = positive_df['Rear Wheel Speed'].mean()
    negative_df = df[df['Rear Wheel Input']<0]
    negative_mean = negative_df['Rear Wheel Speed'].mean()
    print(f'Positive Cycle Mean: {positive_mean}')
    print(f'Negative Cycle Mean: {negative_mean}')
    print(positive_df.describe())
    print(negative_df.describe())
    print(df.describe())

    # Plotting Angle vs Time #
    fig, axs = plt.subplots(2, 1)
    fig.set_figheight(10)
    fig.set_figwidth(12)

    # Plot on the first axis
    axs[0].plot(df['Time'], df['Rear Wheel Input'])
    axs[0].set_xlabel('Time')
    axs[0].set_ylabel('Input Speed')

    # Plot on the second axis
    axs[1].plot(df['Time'], df['Rear Wheel Speed'])
    axs[1].set_xlabel('Time')
    axs[1].set_ylabel('Encoder Speed')

    # Show the plot
    plt.show()

# Plotting Sensor Value Readings #
def plot_from_csv_front():
    # Reading CSV into pandas DataFrame #
    df = pd.read_csv(FRONT_PATH)

    # Printing Statistics of DataFrame #
    positive_df = df[df['Front Wheel Input']>0]
    positive_mean = positive_df['Front Wheel Speed'].mean()
    negative_df = df[df['Front Wheel Input']<0]
    negative_mean = negative_df['Front Wheel Speed'].mean()
    print(f'Positive Cycle Mean: {positive_mean}')
    print(f'Negative Cycle Mean: {negative_mean}')
    print(positive_df.describe())
    print(negative_df.describe())
    print(df.describe())

    # Plotting Angle vs Time #
    fig, axs = plt.subplots(2, 1)
    fig.set_figheight(10)
    fig.set_figwidth(12)

    # Plot on the first axis
    axs[0].plot(df['Time'], df['Front Wheel Input'])
    axs[0].set_xlabel('Time')
    axs[0].set_ylabel('Input Speed')

    # Plot on the second axis
    axs[1].plot(df['Time'], df['Front Wheel Speed'])
    axs[1].set_xlabel('Time')
    axs[1].set_ylabel('Encoder Speed')

    # Show the plot
    plt.show()

# Function to Read Accelerometer, Complimentary Filter, Kalman Filter Angles #
def read_from_serial_rear():
    # Adding Header Row with Columns of CSV #
    with open(REAR_PATH, mode='w') as sensor_file:
        sensor_writer = csv.writer(
                sensor_file, 
                delimiter=',', 
                quotechar='"', 
                quoting=csv.QUOTE_MINIMAL
                )
        # sensor_writer.writerow(['Time','Rear Wheel Input','Rear Wheel Ticks','Rear Wheel Speed'])
        sensor_writer.writerow(['Time','Rear Wheel Input','Rear Wheel Ticks','Rear Wheel Speed'])
    
    # Creating Serial Object for COM Port and Selected Baud Rate #
    x = serial.Serial(COM, BAUD, timeout=0.1)

    # Reading Serial Values and Storing into CSV #
    while x.isOpen() is True:
        data = x.readline().decode('utf-8')
        print(data)
        data = str(x.readline().decode('utf-8')).rstrip()
        if data != '':
            with open(REAR_PATH, mode='a') as sensor_file:
                line = data.split(',')
                sensor_writer = csv.writer(
                        sensor_file, 
                        delimiter=',', 
                        quotechar='"', 
                        quoting=csv.QUOTE_MINIMAL
                        )
                sensor_writer.writerow([line[0],line[1],line[2],line[3]])

def read_from_serial_front():
# Adding Header Row with Columns of CSV #
    with open(FRONT_PATH, mode='w') as sensor_file:
        sensor_writer = csv.writer(
                sensor_file, 
                delimiter=',', 
                quotechar='"', 
                quoting=csv.QUOTE_MINIMAL
                )
        # sensor_writer.writerow(['Time','Rear Wheel Input','Rear Wheel Ticks','Rear Wheel Speed'])
        sensor_writer.writerow(['Time','Front Wheel Input','Front Wheel Ticks','Front Wheel Speed'])
    
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
    # read_from_serial_rear()
    # read_from_serial_front()
    # plot_from_csv_rear()
    plot_from_csv_front()