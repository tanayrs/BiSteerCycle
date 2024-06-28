import serial
import time
import csv
from matplotlib import pyplot as plt
import pandas as pd

# Defining Path to CSV File, Com Port and Baud Rate #
PATH = './Python/filter testing/SensorData/BNO_Test_Step_17.csv'
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
    plt.plot(df['Relative time'],df['SFA'])
    plt.plot(df['Relative time'],df['Kalman'])
    # plt.axhline(y=90,linestyle='--',linewidth=0.75)
    # plt.axhline(y=0,linestyle='--', color='k',linewidth=0.75)

def chosen_plots():
    loop_path = './Python/filter testing/SensorData/BNO_Test_Step_'
    plot_nums = [7,13,17]
    plot_max = [77, 74, 75]
    plot_end_time = [6978, 4292, 3840]
    plot_step_time = [2540, 1243, 973]
    angle_offsets = [1.25, 1.05, 0.58]
    for i in range(3):
        temp_path = loop_path + str(plot_nums[i]) + '.csv'
        plot_from_csv(temp_path)
        plt.hlines(y=plot_max[i],xmin=0,xmax=plot_step_time[i], color='tab:gray', linestyle='--',linewidth=1)
        plt.vlines(x=plot_step_time[i],ymin=angle_offsets[i],ymax=plot_max[i], color='tab:gray', linestyle='--',linewidth=1)
        plt.hlines(y=angle_offsets[i],xmin=plot_step_time[i],xmax=plot_end_time[i], color='tab:gray', linestyle='--',linewidth=1)
        plt.legend(['SFA', 'Kalman', 'Step Input'])
        plt.xlabel('Time (ms)', fontsize=14)
        plt.ylabel('Angle (degrees)', fontsize=14)
        plt.title('Comparison of Step Response of SFA and Kalman Filter', fontsize=14)
        plt.show()


if __name__ == '__main__':
    # read_from_serial()
    chosen_plots()
    # loop_path = './Python/filter testing/SensorData/BNO_Test_Step_'
    # # plot_from_csv()
    # for i in range(1,21):
    #     plt.subplot(4,5,i)
    #     temp_path = loop_path + str(i) + '.csv'
    #     print(temp_path)
    #     plot_from_csv(temp_path)
    #     if i % 5 == 1:
    #         plt.ylabel('Angle (degrees)', fontsize=14)
    #     if i > 15:
    #         plt.xlabel('Time (ms)', fontsize=14)
    #     if i == 5:
    #         plt.legend(['SFA', 'Kalman'])

    # plt.suptitle('Step Response of Bosch Sensor Fusion Algorithm and Kalman Filters',fontsize=18)
    # plt.show()
    # # plot_from_csv(PATH)