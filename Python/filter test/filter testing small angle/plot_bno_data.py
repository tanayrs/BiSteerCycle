import serial
import time
import csv
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import os

# Defining Path to CSV File, Com Port and Baud Rate #
COM = '/dev/cu.usbmodem160229201'
BAUD = 9600

# Function to Read Accelerometer, Complimentary Filter, Kalman Filter Angles #
def read_from_serial(path,overwrite=False):
    if not overwrite and os.path.exists(path):
        print('File Already Exists, Try Again')
        return
   
    # Adding Header Row with Columns of CSV #
    with open(path, mode='w') as sensor_file:
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
            with open(path, mode='a') as sensor_file:
                line = data.split(' ')
                sensor_writer = csv.writer(
                        sensor_file, 
                        delimiter=',', 
                        quotechar='"', 
                        quoting=csv.QUOTE_MINIMAL
                        )
                sensor_writer.writerow([line[0],line[1],line[2],line[3]])

# Plots Sensor Value Readings #
def plot_from_csv(path,settle_time_kal, settle_time_sfa, step_time):
    # Reading CSV into pandas DataFrame #
    df = pd.read_csv(path)

    # Printing Statistics of DataFrame #
    # print(df.describe())

    # Plotting Angle vs Time #
    df['Relative Time'] = df['Time'] - df['Time'][0]
    plt.plot(df['Relative Time'],df['SFA'], label='SFA')
    plt.plot(df['Relative Time'],df['Kalman'], label='Kalman')

    plt.axvline(x=settle_time_kal+step_time, color='tab:orange', linestyle='--', linewidth=1,label='Settling Time Kal')
    plt.axvline(x=settle_time_sfa+step_time, color='tab:blue', linestyle='--', linewidth=1,label='Settling Time SFA')
    # plt.axvline(x=step_time, color='black', linestyle='--', linewidth=1, label='Step time')

    xticks = [i for i in range(0,df['Relative Time'].iloc[-1],200) if np.abs(i-settle_time_kal-step_time) > 100 and np.abs(i-settle_time_sfa-step_time) > 100]
    xticks.extend([settle_time_kal+step_time, settle_time_sfa+step_time])
    plt.xticks(xticks)

# Plots all the Sensor reading plots individually
def small_angle_plots():
    DATA_PATH = './Python/filter test/filter testing small angle/SensorData'
    files = [f for f in os.listdir(DATA_PATH) if os.path.isfile(os.path.join(DATA_PATH,f))]
    for path in files:
        path = os.path.join(DATA_PATH,path)
        settle_time_kal,_,settle_time_sfa,_,step_time,_,_ = find_overshoot(path)
        plot_from_csv(path, settle_time_kal, settle_time_sfa, step_time)
        plt.legend(fontsize=14)
        plt.xlabel('Time (ms)', fontsize=14)
        plt.ylabel('Angle (degrees)', fontsize=14)
        plt.title('Comparison of Step Response of SFA and Kalman Filter', fontsize=16)
        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle()
        plt.show()

# Finds overshoot and settling time for the Kalman filter and SFA
def find_overshoot(path):
    # First Task: Find Range of Motion, First Value in DataFrame, Subtract From Last Value In DataFrame
    # Find min value of dataframe, compare with final settled value, difference is overshoot #
    # Next Find Time Point of Start of Step, Then find point where it reaches with 2% of range within final value #
    df = pd.read_csv(path)
    df['Relative Time'] = df['Time'] - df['Time'].iloc[0]

    max_angle_sfa = df['SFA'].iloc[0]
    max_angle_kal = df['Kalman'].iloc[0]
    settle_angle_sfa = df['SFA'].iloc[-1]
    settle_angle_kal = df['Kalman'].iloc[-1]

    angle_range_sfa = max_angle_sfa - settle_angle_sfa
    angle_range_kal = max_angle_kal - settle_angle_kal

    print(f'{max_angle_sfa=}, {settle_angle_sfa=}, {angle_range_sfa=}')
    ## Finding Overshot of SFA and Kalman ##
    os_per_sfa = 100*np.abs(df['SFA'].min() - settle_angle_sfa)/angle_range_sfa
    os_per_kal = 100*np.abs(df['Kalman'].min() - settle_angle_kal)/angle_range_kal

    ## Finding Settling Time of SFA and Kalman ##
    settle_time_sfa = np.inf
    settle_time_kal = np.inf

    step_time = np.inf

    for _,row in df.iterrows():
        subset = df[df['Relative Time']>row['Relative Time']]
        
        # print(f"{subset['SFA'].min()=},{subset['Kalman'].min()=},{settle_angle_sfa=},{settle_angle_kal=},{0.1*angle_range_sfa=},{0.1*angle_range_kal=}")
        
        if step_time == np.inf and (max_angle_sfa-row['SFA']) > 0.5:
            step_time = row['Relative Time']
        
        sfa_angle_diff_max = np.abs(settle_angle_sfa - subset['SFA'].max())
        sfa_angle_diff_min = np.abs(settle_angle_sfa - subset['SFA'].min())
        
        if settle_time_sfa == np.inf and sfa_angle_diff_max < 0.02*angle_range_sfa and sfa_angle_diff_min < 0.02*angle_range_sfa:
            settle_time_sfa = row['Relative Time'] - step_time
        
        if settle_time_kal == np.inf and np.abs(settle_angle_kal - subset['Kalman'].min()) < 0.02*angle_range_kal and np.abs(settle_angle_kal - subset['Kalman'].max()) < 0.02*angle_range_kal:
            settle_time_kal = row['Relative Time'] - step_time
    
    # print(f'{settle_time_kal=}, {settle_time_sfa=}')
    # print(f'{os_per_kal=}, {os_per_sfa=}')
    return settle_time_kal,os_per_kal,settle_time_sfa,os_per_sfa, step_time, max_angle_sfa, settle_angle_sfa

# Scatterplot of settling time and overshoot for all sensor value reading instances
def plot_comparison(DATA_PATH):
    files = [f for f in os.listdir(DATA_PATH) if os.path.isfile(os.path.join(DATA_PATH,f))]
    print(files)
    settle_times_kal = []
    os_percs_kal = []
    settle_times_sfa = []
    os_percs_sfa = []
    
    for file in files:
        path = os.path.join(DATA_PATH,file)
        settle_time_kal,os_per_kal,settle_time_sfa,os_per_sfa,_,_,_ = find_overshoot(path)
        settle_times_kal.append(settle_time_kal)
        os_percs_kal.append(os_per_kal)
        settle_times_sfa.append(settle_time_sfa)
        os_percs_sfa.append(os_per_sfa)

    plt.scatter(
        settle_times_sfa,os_percs_sfa,
        color='tab:purple',
        marker='o',
        s=80,
        label='SFA'
    )
    plt.scatter(
        settle_times_kal,os_percs_kal,
        color='tab:green',
        marker='x',
        linewidths=3,
        s=80,
        label='Kalman Filter'
    )
    plt.xlabel('Settling Time (ms)',fontsize=14)
    plt.ylabel('Max Overshoot (%)',fontsize=14)
    plt.xscale(value='log')
    plt.title("Settling time and Overshoot for Kalman filter and SFA", fontsize=16)
    plt.legend(fontsize=14)
    manager=plt.get_current_fig_manager()
    manager.full_screen_toggle()
    plt.grid()
    plt.show()

# Plots all the Sensor readings in a single figure
def all_plots():
    loop_path = './Python/filter test/filter testing small angle/SensorData/BNO_Test_Step_'
    for i in range(1,11):
        plt.subplot(2,5,i)
        temp_path = loop_path + str(i) + '.csv'
        settle_time_kal,_,settle_time_sfa,_,step_time,_,_ = find_overshoot(temp_path)
        plot_from_csv(temp_path, settle_time_kal, settle_time_sfa, step_time)
        if i % 5 == 1:
            plt.ylabel('Angle (degrees)', fontsize=14)
        if i > 5:
            plt.xlabel('Time (ms)', fontsize=14)
        if i == 5:
            plt.legend(fontsize=10, loc='upper right')

    plt.suptitle('Comparison of Step Response of SFA and Kalman Filter', fontsize=16)
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    plt.show()


if __name__ == '__main__':
    path = './Python/filter test/filter testing small angle/SensorData/BNO_Test_Step_10.csv'
    
    # try:
    #     read_from_serial(path)
    # except:
    #     pass

    small_angle_plots()
    # all_plots()  
    
    # DATA_PATH = './Python/filter test/filter testing small angle/SensorData'
    # plot_comparison(DATA_PATH)

