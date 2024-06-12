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

PATH = './Python/dead band/RearDeadBandData.csv'
COM = '/dev/cu.usbmodem160464801'
BAUD = 115200

REAR_TIME_DEADBAND_START = 16752
REAR_TIME_DEADBAND_END = 20690
REAR_SPEED_DEADBAND_START = -8
REAR_SPEED_DEADBAND_END = 12

# Reads Rear Wheel Data from Serial Channel and Stores to CSV #
def read_from_serial():
    # Adding Header Row with Columns of CSV #
    with open(PATH, mode='w') as sensor_file:
        sensor_writer = csv.writer(
                sensor_file, 
                delimiter=',', 
                quotechar='"', 
                quoting=csv.QUOTE_MINIMAL
                )
        sensor_writer.writerow(["Time", "Rear Wheel Input", "Rear Wheel Ticks"])
    
    # Creating Serial Object for COM Port and Selected Baud Rate #
    x = serial.Serial()
    x.port = COM
    x.baudrate = BAUD
    x.timeout = 1
    x.setDTR(False)
    #x.setRTS(False)
    x.open()

    # Reading Serial Values and Storing into CSV #
    while x.isOpen() is True:
        data = str(x.readline().decode('utf-8')).rstrip()
        print(data.split(r'\w'))
        # if data != '':
        #     with open(PATH, mode='a') as sensor_file:
        #         line = data.split(' ')
        #         sensor_writer = csv.writer(
        #                 sensor_file, 
        #                 delimiter=',', 
        #                 quotechar='"', 
        #                 quoting=csv.QUOTE_MINIMAL
        #                 )
        #         sensor_writer.writerow([line[0],line[1],line[2]])

# Plotting Sensor Value Readings #
def plot_from_csv():
    # Reading CSV into pandas DataFrame #
    df = pd.read_csv(PATH)

    # Printing Statistics of DataFrame #
    print(df.describe())

    # Plotting Angle vs Time #
    fig, axs = plt.subplots(2, 1)
    fig.set_figheight(10)
    fig.set_figwidth(12)

    # Plot on the first axis
    axs[0].plot(df['Time'], df['Rear Wheel Input'])
    axs[0].axvline(x=REAR_TIME_DEADBAND_START, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=REAR_TIME_DEADBAND_END, color='k', linestyle='--', linewidth=0.5)
    axs[0].axhline(y=REAR_SPEED_DEADBAND_START, color='k', linestyle='--', linewidth=0.5)
    axs[0].axhline(y=REAR_SPEED_DEADBAND_END, color='k', linestyle='--', linewidth=0.5)
    axs[0].set_xlabel('Time')
    axs[0].set_ylabel('Input Speed')
    axs[0].set_yticks(np.arange(-50,50,step=5))

    # Plot on the second axis
    axs[1].plot(df['Time'], df['Rear Wheel Ticks'])
    axs[1].axvline(x=REAR_TIME_DEADBAND_START, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=REAR_TIME_DEADBAND_END, color='k', linestyle='--', linewidth=0.5)
    axs[1].set_xlabel('Time')
    axs[1].set_ylabel('Encoder Ticks')

    # Show the plot
    plt.show()


    # Plotting Graph #
    plt.show()

if __name__ == '__main__':
    # read_from_serial()
    plot_from_csv()