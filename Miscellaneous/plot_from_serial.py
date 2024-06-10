import serial
import time
import csv
from matplotlib import pyplot as plt
import pandas as pd

PATH = 'SpeedData.csv'
COM = '/dev/cu.usbmodem160464801'
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
        sensor_writer.writerow(["Time", "Front Angle", "Rear Angle"])
    
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
                sensor_writer.writerow([line[0],line[1],line[2]])

# Plotting Sensor Value Readings #
def plot_from_csv():
    # Reading CSV into pandas DataFrame #
    df = pd.read_csv(PATH)

    # Printing Statistics of DataFrame #
    print(df.describe())

    # Plotting Angle vs Time #
    plt.plot(df['Time'],df['Front Angle'])
    plt.plot(df['Time'],df['Front Angle'])

    plt.xlabel('Time')
    plt.ylabel('Angle')
    plt.legend(['Front Angle','Rear Angle'])

    # Setting y-limits to +- 6*std #
    front_angle_mean = df['Front Angle'].mean()
    front_angle_std = df['Rear Angle'].std()
    rear_angle_mean = df['Front Angle'].mean()
    rear_angle_std = df['Rear Angle'].std()
    # plt.ylim(
    #         [max(abs(front_angle_mean),abs(rear_angle_mean)) - (6*max(abs(front_angle_std),abs(rear_angle_std))), 
    #          max(abs(front_angle_mean),abs(rear_angle_mean)) - (6*max(abs(front_angle_std),abs(rear_angle_std)))]
    # )

    # Plotting Graph #
    plt.show()

if __name__ == '__main__':
    #read_from_serial()
    plot_from_csv()
