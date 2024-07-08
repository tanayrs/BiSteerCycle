'''
Experiment: Dead Band Testing
By: Jia Bhargava, Tanay Srinivasa
Last Modified: 12 June 2024

Run bi_steer_cycle arduino code with set_dead_band_speed()
'''

import serial
import time
import csv
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

TRIANGLE_REAR_SPEED_PATH = './Python/deadband tests/deadband 8bit/SourceData/older_data/TriangleRearDeadBandDataSpeed.csv'
COM = '/dev/cu.usbmodem160464801'
BAUD = 115200

TRIANGLE_REAR_SPEED_TIME_DEADBAND_START_UNSCALED_1 = 250727
TRIANGLE_REAR_SPEED_TIME_DEADBAND_END_UNSCALED_1 = 253569
TRIANGLE_REAR_SPEED_TIME_DEADBAND_START_UNSCALED_2 = 271125
TRIANGLE_REAR_SPEED_TIME_DEADBAND_END_UNSCALED_2 = 274913
TRIANGLE_REAR_SPEED_TIME_DEADBAND_START_UNSCALED_3 = 2.9218e+05
TRIANGLE_REAR_SPEED_TIME_DEADBAND_END_UNSCALED_3 = 2.9550e+05
TRIANGLE_REAR_SPEED_TIME_DEADBAND_START_UNSCALED_4 = 3.1339e+05
TRIANGLE_REAR_SPEED_TIME_DEADBAND_END_UNSCALED_4 = 3.1726e+05
TRIANGLE_REAR_SPEED_DEADBAND_UNSCALED_START = -9
TRIANGLE_REAR_SPEED_DEADBAND_UNSCALED_END = 11


TRIANGLE_FRONT_SPEED_TIME_DEADBAND_START_UNSCALED_1 = 376882
TRIANGLE_FRONT_SPEED_TIME_DEADBAND_END_UNSCALED_1 = 380264
TRIANGLE_FRONT_SPEED_TIME_DEADBAND_START_UNSCALED_2 = 397929
TRIANGLE_FRONT_SPEED_TIME_DEADBAND_END_UNSCALED_2 = 401393
TRIANGLE_FRONT_SPEED_TIME_DEADBAND_START_UNSCALED_3 = 418947
TRIANGLE_FRONT_SPEED_TIME_DEADBAND_END_UNSCALED_3 = 422848
TRIANGLE_FRONT_SPEED_TIME_DEADBAND_START_UNSCALED_4 = 440304
TRIANGLE_FRONT_SPEED_TIME_DEADBAND_END_UNSCALED_4 = 443763
TRIANGLE_FRONT_SPEED_DEADBAND_UNSCALED_START = -11
TRIANGLE_FRONT_SPEED_DEADBAND_UNSCALED_END = 11

class Motor:
    def __init__(self,path,deadband_starts, deadband_ends, deadband_inputs):
        self.df = pd.read_csv(path)
        self.deadband_starts = deadband_starts
        self.deadband_ends = deadband_ends
        self.deadband_inputs = deadband_inputs
    
    def plot(self):
        # Plotting Angle vs Time #
        fig, axs = plt.subplots(2, 1)
        fig.set_figheight(10)
        fig.set_figwidth(12)

        # Plot on the first axis
        axs[0].plot(self.df['Time'], self.df['Wheel Input'])
        for start in self.deadband_starts:
            axs[0].axvline(x=start, color='k', linestyle='--', linewidth=0.5)
        for input in self.deadband_inputs:
            axs[0].axhline(y=input, color='k', linestyle='--', linewidth=0.5)
        for end in self.deadband_ends:
            axs[0].axvline(x=end, color='k', linestyle='--', linewidth=0.5)
        axs[0].set_xlabel('Time')
        axs[0].set_ylabel('Input Speed')
        axs[0].set_yticks(np.arange(-50,50,step=5))

        # Plot on the second axis
        axs[1].plot(self.df['Time'], self.df['Wheel Speed'])
        for start in self.deadband_starts:
            axs[1].axvline(x=start, color='k', linestyle='--', linewidth=0.5)
        for end in self.deadband_ends:
            axs[1].axvline(x=end, color='k', linestyle='--', linewidth=0.5)
        axs[1].set_xlabel('Time')
        axs[1].set_ylabel('Encoder Speed')

        # Show the plot
        plt.show()
    
    def plot_ticks(self):
        # Plotting Angle vs Time #
        fig, axs = plt.subplots(2, 1)
        fig.set_figheight(10)
        fig.set_figwidth(12)

        # Plot on the first axis
        axs[0].plot(self.df['Time'], self.df['Wheel Input'])
        for start in self.deadband_starts:
            axs[0].axvline(x=start, color='k', linestyle='--', linewidth=0.5)
        for input in self.deadband_inputs:
            axs[0].axhline(y=input, color='k', linestyle='--', linewidth=0.5)
        for end in self.deadband_ends:
            axs[0].axvline(x=end, color='k', linestyle='--', linewidth=0.5)
        axs[0].set_xlabel('Time')
        axs[0].set_ylabel('Input Speed')
        axs[0].set_yticks(np.arange(-50,50,step=5))

        # Plot on the second axis
        axs[1].plot(self.df['Time'], self.df['Wheel Ticks'])
        for start in self.deadband_starts:
            axs[1].axvline(x=start, color='k', linestyle='--', linewidth=0.5)
        for end in self.deadband_ends:
            axs[1].axvline(x=end, color='k', linestyle='--', linewidth=0.5)
        axs[1].set_xlabel('Time')
        axs[1].set_ylabel('Encoder Ticks')

        # Show the plot
        plt.show()

def plot_from_csv_rear():
    path = './Python/deadband tests/deadband 8bit/SourceData/older_data/RearDeadBandData.csv'
    starts = [16752]
    ends = [20690]
    inputs = [-8, 12]

    obj = Motor(path,starts,ends,inputs)

    obj.plot_ticks()

def plot_from_csv_front():
    path = './Python/deadband tests/deadband 8bit/SourceData/older_data/FrontDeadBandData.csv'

    starts = [36762]
    ends = [41905]
    inputs = [-10, 15]

    obj = Motor(path, starts, ends, inputs)
    obj.plot_ticks()

def plot_from_csv_front_speed():
    path = './Python/deadband tests/deadband 8bit/SourceData/older_data/FrontDeadBandDataSpeed.csv'
    starts = [59185]
    ends = [62884]
    inputs = [-7, 11]
    
    obj = Motor(path, starts, ends, inputs)
    obj.plot()

def plot_from_csv_rear_speed():
    path = './Python/deadband tests/deadband 8bit/SourceData/older_data/RearDeadBandDataSpeed.csv'
    starts = [16747]
    ends = [20879]
    inputs = [-9, 11]
    obj = Motor(path,starts,ends,inputs)
    obj.plot()

def plot_from_csv_rear_speed_triangle_unscaled():
    path = './Python/deadband tests/deadband 8bit/SourceData/TriangleFrontDeadBandDataSpeed.csv'
    starts = [418599, 439726, 461058]
    ends = [422400, 443302, 4.6444e+05]
    inputs = [-9, 11]
    obj = Motor(path, starts, ends, inputs)
    obj.plot()
    return
    # Reading CSV into pandas DataFrame #
    df = pd.read_csv(TRIANGLE_REAR_SPEED_PATH)

    # Printing Statistics of DataFrame #
    print(df.describe())

    # Plotting Angle vs Time #
    fig, axs = plt.subplots(2, 1)
    fig.set_figheight(10)
    fig.set_figwidth(12)

    # Plot on the first axis
    axs[0].plot(df['Time'], df['Rear Wheel Input'])
    axs[0].axvline(x=TRIANGLE_REAR_SPEED_TIME_DEADBAND_START_UNSCALED_1, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=TRIANGLE_REAR_SPEED_TIME_DEADBAND_END_UNSCALED_1, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=TRIANGLE_REAR_SPEED_TIME_DEADBAND_START_UNSCALED_2, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=TRIANGLE_REAR_SPEED_TIME_DEADBAND_END_UNSCALED_2, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=TRIANGLE_REAR_SPEED_TIME_DEADBAND_START_UNSCALED_3, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=TRIANGLE_REAR_SPEED_TIME_DEADBAND_END_UNSCALED_3, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=TRIANGLE_REAR_SPEED_TIME_DEADBAND_START_UNSCALED_4, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=TRIANGLE_REAR_SPEED_TIME_DEADBAND_END_UNSCALED_4, color='k', linestyle='--', linewidth=0.5)
    axs[0].axhline(y=REAR_SPEED_DEADBAND_START, color='k', linestyle='--', linewidth=0.5)
    axs[0].axhline(y=REAR_SPEED_DEADBAND_END, color='k', linestyle='--', linewidth=0.5)
    axs[0].set_ylabel('Input Speed (PWM Value)',fontsize=14)
    axs[0].set_yticks([-50,-40,-30,-20,-10,-5,5,10,20,30,40,50])
    axs[0].set_xticks([])

    # Plot on the second axis
    axs[1].plot(df['Time'], df['Rear Wheel Speed'])
    axs[1].axvline(x=TRIANGLE_REAR_SPEED_TIME_DEADBAND_START_UNSCALED_1, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=TRIANGLE_REAR_SPEED_TIME_DEADBAND_END_UNSCALED_1, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=TRIANGLE_REAR_SPEED_TIME_DEADBAND_START_UNSCALED_2, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=TRIANGLE_REAR_SPEED_TIME_DEADBAND_END_UNSCALED_2, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=TRIANGLE_REAR_SPEED_TIME_DEADBAND_START_UNSCALED_3, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=TRIANGLE_REAR_SPEED_TIME_DEADBAND_END_UNSCALED_3, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=TRIANGLE_REAR_SPEED_TIME_DEADBAND_START_UNSCALED_4, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=TRIANGLE_REAR_SPEED_TIME_DEADBAND_END_UNSCALED_4, color='k', linestyle='--', linewidth=0.5)
    axs[1].set_xlabel('Time (ms)',fontsize=14)
    axs[1].set_ylabel('Encoder Speed (Degrees per Second)',fontsize=14)

    # Show the plot
    plt.tight_layout()
    plt.show()

def plot_from_csv_rear_speed_triangle_unscaled_corrected():
    # Reading CSV into pandas DataFrame #
    df = pd.read_csv(TRIANGLE_REAR_SPEED_PATH)

    # Printing Statistics of DataFrame #
    print(df.describe())

    # Plotting Angle vs Time #
    fig, axs = plt.subplots(2, 1)
    fig.set_figheight(10)
    fig.set_figwidth(12)

    # Plot on the first axis
    axs[0].plot(df['Time'], df['Rear Wheel Input'])
    # axs[0].axvline(x=TRIANGLE_REAR_SPEED_TIME_DEADBAND_START_UNSCALED_1, color='k', linestyle='--', linewidth=0.5)
    # axs[0].axvline(x=TRIANGLE_REAR_SPEED_TIME_DEADBAND_END_UNSCALED_1, color='k', linestyle='--', linewidth=0.5)
    # axs[0].axvline(x=TRIANGLE_REAR_SPEED_TIME_DEADBAND_START_UNSCALED_2, color='k', linestyle='--', linewidth=0.5)
    # axs[0].axvline(x=TRIANGLE_REAR_SPEED_TIME_DEADBAND_END_UNSCALED_2, color='k', linestyle='--', linewidth=0.5)
    # axs[0].axvline(x=TRIANGLE_REAR_SPEED_TIME_DEADBAND_START_UNSCALED_3, color='k', linestyle='--', linewidth=0.5)
    # axs[0].axvline(x=TRIANGLE_REAR_SPEED_TIME_DEADBAND_END_UNSCALED_3, color='k', linestyle='--', linewidth=0.5)
    # axs[0].axvline(x=TRIANGLE_REAR_SPEED_TIME_DEADBAND_START_UNSCALED_4, color='k', linestyle='--', linewidth=0.5)
    # axs[0].axvline(x=TRIANGLE_REAR_SPEED_TIME_DEADBAND_END_UNSCALED_4, color='k', linestyle='--', linewidth=0.5)
    # axs[0].axhline(y=REAR_SPEED_DEADBAND_START, color='k', linestyle='--', linewidth=0.5)
    # axs[0].axhline(y=REAR_SPEED_DEADBAND_END, color='k', linestyle='--', linewidth=0.5)
    axs[0].set_ylabel('Input Speed (PWM Value)',fontsize=14)
    axs[0].set_yticks([-50,-40,-30,-20,-10,-5,5,10,20,30,40,50])
    axs[0].set_xticks([])

    # Plot on the second axis
    axs[1].plot(df['Time'], df['Rear Wheel Speed'])
    # axs[1].axvline(x=TRIANGLE_REAR_SPEED_TIME_DEADBAND_START_UNSCALED_1, color='k', linestyle='--', linewidth=0.5)
    # axs[1].axvline(x=TRIANGLE_REAR_SPEED_TIME_DEADBAND_END_UNSCALED_1, color='k', linestyle='--', linewidth=0.5)
    # axs[1].axvline(x=TRIANGLE_REAR_SPEED_TIME_DEADBAND_START_UNSCALED_2, color='k', linestyle='--', linewidth=0.5)
    # axs[1].axvline(x=TRIANGLE_REAR_SPEED_TIME_DEADBAND_END_UNSCALED_2, color='k', linestyle='--', linewidth=0.5)
    # axs[1].axvline(x=TRIANGLE_REAR_SPEED_TIME_DEADBAND_START_UNSCALED_3, color='k', linestyle='--', linewidth=0.5)
    # axs[1].axvline(x=TRIANGLE_REAR_SPEED_TIME_DEADBAND_END_UNSCALED_3, color='k', linestyle='--', linewidth=0.5)
    # axs[1].axvline(x=TRIANGLE_REAR_SPEED_TIME_DEADBAND_START_UNSCALED_4, color='k', linestyle='--', linewidth=0.5)
    # axs[1].axvline(x=TRIANGLE_REAR_SPEED_TIME_DEADBAND_END_UNSCALED_4, color='k', linestyle='--', linewidth=0.5)
    axs[1].set_xlabel('Time (ms)',fontsize=14)
    axs[1].set_ylabel('Encoder Speed (Degrees per Second)',fontsize=14)

    # Show the plot
    plt.tight_layout()
    plt.show()
    
def plot_from_csv_front_speed_triangle_unscaled():
    # Reading CSV into pandas DataFrame #
    df = pd.read_csv(TRIANGLE_FRONT_SPEED_PATH)

    # Printing Statistics of DataFrame #
    print(df.describe())

    # Plotting Angle vs Time #
    fig, axs = plt.subplots(2, 1)
    fig.set_figheight(10)
    fig.set_figwidth(12)

    # Plot on the first axis
    axs[0].plot(df['Time'], df['Front Wheel Input'])
    axs[0].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_START_UNSCALED_1, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_END_UNSCALED_1, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_START_UNSCALED_2, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_END_UNSCALED_2, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_START_UNSCALED_3, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_END_UNSCALED_3, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_START_UNSCALED_4, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_END_UNSCALED_4, color='k', linestyle='--', linewidth=0.5)
    axs[0].axhline(y=TRIANGLE_FRONT_SPEED_DEADBAND_UNSCALED_START, color='k', linestyle='--', linewidth=0.5)
    axs[0].axhline(y=TRIANGLE_FRONT_SPEED_DEADBAND_UNSCALED_END, color='k', linestyle='--', linewidth=0.5)
    axs[0].set_ylabel('Input Speed (PWM Value)',fontsize=14)
    axs[0].set_yticks([-50,-40,-30,-20,-10,-5,5,10,20,30,40,50])
    axs[0].set_xticks([])

    # Plot on the second axis
    axs[1].plot(df['Time'], df['Front Wheel Speed'])
    axs[1].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_START_UNSCALED_1, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_END_UNSCALED_1, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_START_UNSCALED_2, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_END_UNSCALED_2, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_START_UNSCALED_3, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_END_UNSCALED_3, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_START_UNSCALED_4, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_END_UNSCALED_4, color='k', linestyle='--', linewidth=0.5)
    axs[1].set_xlabel('Time (ms)',fontsize=14)
    axs[1].set_ylabel('Encoder Speed (Degrees per Second)',fontsize=14)

    # Show the plot
    plt.tight_layout()
    plt.show()

def plot_from_csv_front_speed_triangle_unscaled_corrected():
    # Reading CSV into pandas DataFrame #
    df = pd.read_csv(TRIANGLE_FRONT_SPEED_PATH)

    # Printing Statistics of DataFrame #
    print(df.describe())

    # Plotting Angle vs Time #
    fig, axs = plt.subplots(2, 1)
    fig.set_figheight(10)
    fig.set_figwidth(12)

    # Plot on the first axis
    axs[0].plot(df['Time'], df['Front Wheel Input'])
    # axs[0].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_START_UNSCALED_1, color='k', linestyle='--', linewidth=0.5)
    # axs[0].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_END_UNSCALED_1, color='k', linestyle='--', linewidth=0.5)
    # axs[0].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_START_UNSCALED_2, color='k', linestyle='--', linewidth=0.5)
    # axs[0].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_END_UNSCALED_2, color='k', linestyle='--', linewidth=0.5)
    # axs[0].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_START_UNSCALED_3, color='k', linestyle='--', linewidth=0.5)
    # axs[0].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_END_UNSCALED_3, color='k', linestyle='--', linewidth=0.5)
    # axs[0].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_START_UNSCALED_4, color='k', linestyle='--', linewidth=0.5)
    # axs[0].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_END_UNSCALED_4, color='k', linestyle='--', linewidth=0.5)
    # axs[0].axhline(y=FRONT_SPEED_DEADBAND_START, color='k', linestyle='--', linewidth=0.5)
    # axs[0].axhline(y=FRONT_SPEED_DEADBAND_END, color='k', linestyle='--', linewidth=0.5)
    axs[0].set_ylabel('Input Speed (PWM Value)',fontsize=14)
    axs[0].set_yticks([-50,-40,-30,-20,-10,-5,5,10,20,30,40,50])
    axs[0].set_xticks([])

    # Plot on the second axis
    axs[1].plot(df['Time'], df['Front Wheel Speed'])
    # axs[1].axvline(x=TRIANGLE_REAR_SPEEDaxs[0].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_START_UNSCALED_1, color='k', linestyle='--', linewidth=0.5)
    # axs[1].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_START_UNSCALED_1, color='k', linestyle='--', linewidth=0.5)
    # axs[1].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_END_UNSCALED_1, color='k', linestyle='--', linewidth=0.5)
    # axs[1].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_START_UNSCALED_2, color='k', linestyle='--', linewidth=0.5)
    # axs[1].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_END_UNSCALED_2, color='k', linestyle='--', linewidth=0.5)
    # axs[1].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_START_UNSCALED_3, color='k', linestyle='--', linewidth=0.5)
    # axs[1].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_END_UNSCALED_3, color='k', linestyle='--', linewidth=0.5)
    # axs[1].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_START_UNSCALED_4, color='k', linestyle='--', linewidth=0.5)
    # axs[1].axvline(x=TRIANGLE_FRONT_SPEED_TIME_DEADBAND_END_UNSCALED_4, color='k', linestyle='--', linewidth=0.5)
    axs[1].set_xlabel('Time (ms)',fontsize=14)
    axs[1].set_ylabel('Encoder Speed (Degrees per Second)',fontsize=14)

    # Show the plot
    plt.tight_layout()
    plt.show()

def read_from_serial(path):
    # Adding Header Row with Columns of CSV #
    with open(path, mode='w') as sensor_file:
        sensor_writer = csv.writer(
                sensor_file, 
                delimiter=',', 
                quotechar='"', 
                quoting=csv.QUOTE_MINIMAL
                )
        sensor_writer.writerow(['Time','Rear Wheel Input','Rear Wheel Ticks','Rear Wheel Speed'])
    
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

def read_from_serial_front():
    # Adding Header Row with Columns of CSV #
    with open(TRIANGLE_FRONT_SPEED_PATH, mode='w') as sensor_file:
        sensor_writer = csv.writer(
                sensor_file, 
                delimiter=',', 
                quotechar='"', 
                quoting=csv.QUOTE_MINIMAL
                )
        sensor_writer.writerow(['Time','Front Wheel Input','Front Wheel Ticks','Front Wheel Speed'])
    
    # Creating Serial Object for COM Port and Selected Baud Rate #
    x = serial.Serial(COM, BAUD, timeout=0.1)

    # Reading Serial Values and Storing into CSV #
    while x.isOpen() is True:
        data = x.readline().decode('utf-8')
        print(data)
        data = str(x.readline().decode('utf-8')).rstrip()
        if data != '':
            with open(TRIANGLE_FRONT_SPEED_PATH, mode='a') as sensor_file:
                line = data.split(',')
                sensor_writer = csv.writer(
                        sensor_file, 
                        delimiter=',', 
                        quotechar='"', 
                        quoting=csv.QUOTE_MINIMAL
                        )
                sensor_writer.writerow([line[0],line[1],line[2],line[3]])

def read_from_serial_rear():
    # Adding Header Row with Columns of CSV #
    with open(TRIANGLE_REAR_SPEED_PATH, mode='w') as sensor_file:
        sensor_writer = csv.writer(
                sensor_file, 
                delimiter=',', 
                quotechar='"', 
                quoting=csv.QUOTE_MINIMAL
                )
        sensor_writer.writerow(['Time','Rear Wheel Input','Rear Wheel Ticks','Rear Wheel Speed'])
    
    # Creating Serial Object for COM Port and Selected Baud Rate #
    x = serial.Serial(COM, BAUD, timeout=0.1)

    # Reading Serial Values and Storing into CSV #
    while x.isOpen() is True:
        data = x.readline().decode('utf-8')
        print(data)
        data = str(x.readline().decode('utf-8')).rstrip()
        if data != '':
            with open(TRIANGLE_REAR_SPEED_PATH, mode='a') as sensor_file:
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
    # plot_from_csv_front()

    # plot_from_csv_front_speed()
    # plot_from_csv_rear_speed()

    plot_from_csv_rear_speed_triangle_unscaled()
    # plot_from_csv_rear_speed_triangle_unscaled_corrected()
    
    # plot_from_csv_front_speed_triangle_unscaled()
    # plot_from_csv_front_speed_triangle_unscaled_corrected()

    # read_from_serial()