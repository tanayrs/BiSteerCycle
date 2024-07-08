import serial
import time
import csv
from matplotlib import pyplot as plt
import pandas as pd

PATH = './Python/motor calibration/motor calibration sinusoidal/SourceData/SpeedData.csv'
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
        sensor_writer.writerow(["Time", "Rear Speed"])
    
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
    df['Relative Time'] = df['Time'] - df['Time'].iloc[0]

    # Printing Statistics of DataFrame #
    print(df.describe())

    # Plotting Front Speed vs Time #
    plt.plot(df['Relative Time'],df['Front Speed'])
    plt.axhline(y=df['Front Speed'].max(),linestyle='--',color='k',linewidth=1)
    plt.axhline(y=df['Front Speed'].min(),linestyle='--',color='k',linewidth=1)
    plt.yticks([-30,df['Front Speed'].min(),-20,-10,0,10,20,df['Front Speed'].max(),30])
    plt.xlabel('Time (ms)')
    plt.ylabel('Speed ($^{o}/s$)')

    # Plotting Graph #
    plt.show()

    # Plotting Rear Speed vs Time #
    plt.plot(df['Relative Time'],df['Rear Speed'])
    plt.axhline(y=df['Rear Speed'].max(),linestyle='--',color='k',linewidth=1)
    plt.axhline(y=df['Rear Speed'].min(),linestyle='--',color='k',linewidth=1)
    plt.yticks([-30,df['Rear Speed'].min(),-20,-10,0,10,20,df['Rear Speed'].max(),30])
    plt.xlabel('Time (ms)')
    plt.ylabel('Speed ($^{o}/s$)')

    # Plotting Graph #
    plt.show()

if __name__ == '__main__':
    # read_from_serial()
    plot_from_csv()