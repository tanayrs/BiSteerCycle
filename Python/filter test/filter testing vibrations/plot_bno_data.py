import serial
import time
import csv
from matplotlib import pyplot as plt
import pandas as pd

# Defining Path to CSV File, Com Port and Baud Rate #
PATH = './Python/filter test/filter testing vibrations/SensorData/vibrations.csv'
COM = '/dev/cu.usbmodem160229201'
BAUD = 9600

# Function to Read Accelerometer, Complimentary Filter, Kalman Filter Angles #
def read_from_serial():
    # Adding Header Row with Columns of CSV #
    with open(PATH, mode='w') as sensor_file:
        sensor_writer = csv.writer(
                sensor_file, 
                delimiter=',', 
                quotechar='"', 
                quoting=csv.QUOTE_MINIMAL
                )
        sensor_writer.writerow(["Time", "Acceleration", "Kalman"])
    
    # Creating Serial Object for COM Port and Selected Baud Rate #
    x = serial.Serial(COM, BAUD, timeout=0.1)

    # Reading Serial Values and Storing into CSV #
    while x.isOpen() is True:
        data = x.readline().decode('utf-8')
        print(data)
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
                sensor_writer.writerow([line[0],line[1],line[2]])

# Plotting Sensor Value Readings #
def plot_from_csv(path=PATH):
    # Reading CSV into pandas DataFrame #
    df = pd.read_csv(path)

    # Printing Statistics of DataFrame #
    print(df.describe())

    # Plotting Angle vs Time #
    df['Relative time'] = df['Time'] - df['Time'][0]
    plt.plot(df['Relative time'],df['Acceleration'])
    plt.plot(df['Relative time'],df['Kalman'])
    plt.legend(['Accelereometer angle', 'Kalman filter angle'],fontsize=14)
    plt.xlabel('Time (ms)', fontsize=14)
    plt.ylabel('Angle (degrees)', fontsize=14)
    plt.title('Response to vibrations', fontsize=16)
    plt.show()



if __name__ == '__main__':
    # read_from_serial()
    plot_from_csv(PATH)