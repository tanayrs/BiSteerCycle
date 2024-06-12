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

PATH = 'RearDeadBandData.csv'
COM = '/dev/cu.usbmodem160464801'
BAUD = 9600

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
        sensor_writer.writerow(["Time", "Rear Wheel Input", "Rear Wheel Speed"])
    
    # Creating Serial Object for COM Port and Selected Baud Rate #
    x = serial.Serial(COM, BAUD, timeout=0.1)

    # Reading Serial Values and Storing into CSV #
    while x.isOpen() is True:
        data = x.readline().decode('utf-8')  # Remove unnecessary str()

        data = str(x.readline().decode('utf-8')).rstrip()
        if data != '':
            with open(PATH, mode='a') as sensor_file:
                line = data.split(' ')
                sensor_writer = csv.writer(
                        sensor_file, 
                        delimiter=',', 
                        quotechar='"', 
                        quoting=csv.QUOTE_MINIMAL
                        )
                sensor_writer.writerow([line[0],line[1]])

# Plotting Sensor Value Readings #
def plot_from_csv():
    # Reading CSV into pandas DataFrame #
    df = pd.read_csv(PATH)

    # Printing Statistics of DataFrame #
    print(df.describe())

    # Plotting Angle vs Time #
    plt.plot(df['Time'],df['Rear Wheel Input'])
    plt.plot(df['Time'],df['Rear Wheel Speed'])

    plt.xlabel('Time')
    plt.ylabel('Speed')
    plt.legend(['Rear Wheel Input', 'Rear Wheel Speed'])

    # Plotting Graph #
    plt.show()

if __name__ == '__main__':
    # read_from_serial()
    plot_from_csv()