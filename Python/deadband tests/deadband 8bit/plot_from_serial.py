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

COM = '/dev/cu.usbmodem160464801'
BAUD = 115200

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
    path = './Python/deadband tests/deadband 8bit/SourceData/older_data/TriangleRearDeadBandDataSpeed.csv'
    starts = [418599, 439726, 461058]
    ends = [422400, 443302, 4.6444e+05]
    inputs = [-9, 11]
    obj = Motor(path, starts, ends, inputs)
    obj.plot()

    path = './Python/deadband tests/deadband 8bit/SourceData/TriangleRearDeadBandDataSpeedUnscaled.csv'
    
    starts = [250727, 271125, 2.9218e+05, 3.1339e+05]
    ends = [253569, 274913, 2.9550e+05, 3.1726e+05]
    inputs = [-9, 11]
    obj = Motor(path, starts, ends, inputs)
    obj.plot()
    
def plot_from_csv_rear_speed_triangle_unscaled_corrected():
    path = './Python/deadband tests/deadband 8bit/SourceData/TriangleRearDeadBandDataSpeedCorrected_3.csv'
    
    obj = Motor(path, [], [], [])
    obj.plot()
    
def plot_from_csv_front_speed_triangle_unscaled():
    path = './Python/deadband tests/deadband 8bit/SourceData/TriangleFrontDeadBandDataSpeed.csv'
    starts =[376882, 397929, 418947, 440304]
    ends = [380264, 401393, 422848, 443763]
    inputs = [-11,11]

    obj = Motor(path,starts,ends,inputs)
    obj.plot()

def plot_from_csv_front_speed_triangle_unscaled_corrected():
    path = './Python/deadband tests/deadband 8bit/SourceData/TriangleFrontDeadBandDataSpeedCorrected_5.csv'

    obj = Motor(path,[],[],[])
    obj.plot()

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

if __name__ == '__main__':
    # read_from_serial()
    
    # plot_from_csv_rear()
    # plot_from_csv_front()

    # plot_from_csv_front_speed()
    # plot_from_csv_rear_speed()

    # plot_from_csv_rear_speed_triangle_unscaled()
    # plot_from_csv_rear_speed_triangle_unscaled_corrected()
    
    # plot_from_csv_front_speed_triangle_unscaled()
    plot_from_csv_front_speed_triangle_unscaled_corrected()
