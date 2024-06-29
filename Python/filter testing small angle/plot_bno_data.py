import serial
import time
import csv
from matplotlib import pyplot as plt
import pandas as pd

# Defining Path to CSV File, Com Port and Baud Rate #
PATH = './Python/filter testing small angle/SensorData/BNO_Test_Step_4.csv'
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
        sensor_writer.writerow(["Time", "Acceleration", "SFA", "Kalman"])
    
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
                sensor_writer.writerow([line[0],line[1],line[2],line[3]])

# Plotting Sensor Value Readings #
def plot_from_csv(path=PATH):
    # Reading CSV into pandas DataFrame #
    df = pd.read_csv(path)

    # Printing Statistics of DataFrame #
    print(df.describe())

    # Plotting Angle vs Time #
    df['Relative time'] = df['Time'] - df['Time'][0]
    plt.plot(df['Relative time'],df['SFA'], label='SFA')
    plt.plot(df['Relative time'],df['Kalman'], label='Kalman')
    # plt.axhline(y=90,linestyle='--',linewidth=0.75)
    # plt.axhline(y=0,linestyle='--', color='k',linewidth=0.75)

def small_angle_plots():
    loop_path = './Python/filter testing small angle/SensorData/BNO_Test_Step_'
    plot_max = [6.5, 5.17, 5.83, 5.4]
    plot_end_time = [8345, 8695, 5212, 16788]
    plot_step_time = [3086, 6866, 2610, 14064]
    angle_offsets = [-1.08, -1.287, -1.23, -1.427]
    for i in range(4):
        plt.hlines(y=plot_max[i],xmin=0,xmax=plot_step_time[i], color='tab:gray', linestyle='--',linewidth=1, label='_nolegend_')
        plt.vlines(x=plot_step_time[i],ymin=angle_offsets[i],ymax=plot_max[i], color='tab:gray', linestyle='--',linewidth=1,label='_nolegend_')
        plt.hlines(y=angle_offsets[i],xmin=plot_step_time[i],xmax=plot_end_time[i], color='tab:gray', linestyle='--',linewidth=1, label='Step Input')
        temp_path = loop_path + str(i+1) + '.csv'
        plot_from_csv(temp_path)
        plt.legend(fontsize=14)
        plt.xlabel('Time (ms)', fontsize=14)
        plt.ylabel('Angle (degrees)', fontsize=14)
        plt.title('Comparison of Step Response of SFA and Kalman Filter', fontsize=14)
        plt.show()


if __name__ == '__main__':
    # read_from_serial()
    small_angle_plots()
    # plot_from_csv(PATH)
    # plt.title('Comparison of Step Response of SFA and Kalman Filter', fontsize=18)
    # plt.legend(fontsize=14)
    # plt.xlabel('Time (ms)', fontsize=14)
    # plt.ylabel('Angle (degrees)', fontsize=14)
    # plt.show()
