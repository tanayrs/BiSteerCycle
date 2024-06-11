import serial
import time
import csv
from matplotlib import pyplot as plt
import pandas as pd

PATH = 'BNO_Test_Vibrations.csv'
COM = '/dev/cu.usbmodem160229201'
BAUD = 9600

def read_from_serial():
    # Adding Header Row with Columns of CSV #
    with open(PATH, mode='w') as sensor_file:
        sensor_writer = csv.writer(
                sensor_file, 
                delimiter=',', 
                quotechar='"', 
                quoting=csv.QUOTE_MINIMAL
                )
        sensor_writer.writerow(["Time", "Acceleration", "Complimentary", "Kalman"])
    
    # Creating Serial Object for COM Port and Selected Baud Rate #
    x = serial.Serial(COM, BAUD, timeout=0.1)

    # Reading Serial Values and Storing into CSV #
    while x.isOpen() is True:
        data = x.readline().decode('utf-8')
        print(data)
        # data = str(x.readline().decode('utf-8')).rstrip()
        if data != '':
            with open(PATH, mode='a') as sensor_file:
                line = data.split(' ')
                sensor_writer = csv.writer(
                        sensor_file, 
                        delimiter=',', 
                        quotechar='"', 
                        quoting=csv.QUOTE_MINIMAL
                        )
                sensor_writer.writerow([line[0],line[1],line[2],line[3]])

# Plotting Sensor Value Readings #
def plot_from_csv():
    # Reading CSV into pandas DataFrame #
    df = pd.read_csv(PATH)

    # Printing Statistics of DataFrame #
    print(df.describe())

    # Plotting Angle vs Time #
    # plt.plot(df['Time'],df['Acceleration'])
    plt.plot(df['Time'],df['Complimentary'])
    plt.plot(df['Time'],df['Kalman'])

    plt.xlabel('Time (ms)')
    plt.ylabel('Angle (degrees)')
    # plt.legend(['Accelerometer','Complimentary Filter', 'Kalman Filter'])
    plt.title('Vibration Test for Complimentary and Kalman Filter')
    plt.legend(['Complimentary Filter', 'Kalman Filter'])

    plt.show()

if __name__ == '__main__':
    # read_from_serial()
    plot_from_csv()
