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
    def __init__(self,path,deadband_starts, deadband_ends, deadband_inputs, slope_ends=None):
        self.df = pd.read_csv(path)
        self.df['Relative Time'] = self.df['Time']-self.df['Time'].iloc[0]
        
        # Correcting Bevel Gear Inaccuracy #
        try:
            self.df['Wheel Speed'] = -self.df['Wheel Speed']/2
        except:
            pass
        
        self.df['Expected Response'] = self.df['Wheel Input'].apply(self.__calculate_expected_output)
        self.deadband_starts = deadband_starts
        self.deadband_ends = deadband_ends
        self.deadband_inputs = deadband_inputs
        if slope_ends == None:
            self.slope_ends = {'negative':self.df['Relative Time'].iloc[-1],
                          'positive':self.df['Relative Time'].iloc[-1]}
        else:
            self.slope_ends = slope_ends
    
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

# Main Plotting Function to Handle Subplots #
    def plot_compensation(self):
        plt.figure(figsize=(14,8.5))
        
        ### Command vs Time Plot ###
        plt.subplot(2,2,1)
        self.__plot_input()

        ### Command Response Plot for decreasing speed ###
        plt.subplot(2,2,2)
        # self.__plot_cr_decreasing()
        # self.__plot_cr_increasing()
        self.__plot_cr_combined()

        # ### Response vs Time Plot ###
        plt.subplot(2,2,3)
        self.__plot_output()

        ### Command Response Plot for Increasing Speed #
        # plt.subplot(2,2,4)
        # self.__plot_cr_increasing()


        ### Plotting Final Graph ###
        plt.tight_layout(pad=1.08, w_pad=0.1, h_pad=0.1)
        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle()
        plt.show()

    def __plot_input(self):
        plt.plot(self.df['Relative Time'], self.df['Wheel Input'])
        
        # Plotting Vertical Lines at Times where deadband is entered and exitted #
        for end in self.deadband_ends:
            plt.axvline(x=end, color='k', linestyle='--', linewidth=0.5)
        for start in self.deadband_starts:
            plt.axvline(x=start, color='k', linestyle='--', linewidth=0.5)
        
        # Plotting Horizontal lines with Input Corresponding to Static and Kinetic Coefficients #
        for input in self.deadband_inputs:
            plt.axhline(y=input, color='k', linestyle='--', linewidth=0.5)
        
        # Calculating Ticks #
        yticks = []
        set_continue = False
        step = (self.df['Wheel Input'].max()-self.df['Wheel Input'].min())/7
        for i in range(int(self.df['Wheel Input'].min()),int(self.df['Wheel Input'].max()),int(step)):
            for input in self.deadband_inputs:
                if abs(i-input) < (self.df['Wheel Input'].max()-self.df['Wheel Input'].min())/7:
                    set_continue = True
            if set_continue == True:
                set_continue = False
                continue
            else:
                yticks.append(i)
        yticks[-1] = self.df['Wheel Input'].max()
        yticks.extend(self.deadband_inputs)
        
        # Adding Axis Labels, y-ticks and sub-plot title #
        plt.ylabel('Commanded Input (PWM Value)',fontsize=14)
        plt.xlabel('Time (ms)', fontsize=14)
        plt.yticks(yticks)
        plt.ylim([self.df['Wheel Input'].min(),self.df['Wheel Input'].max()])
        # plt.legend(loc='upper right', fontsize=14)
        plt.title('Input', fontsize=18)

    def __plot_output(self):
        ### Command vs Time Plot ###
        plt.plot(self.df['Relative Time'], self.df['Wheel Speed'], label='Measured Response')
        plt.plot(self.df['Relative Time'], self.df['Expected Response'], label='Ideal Response', color='gray')

        # Plotting Vertical Dotted Lines for Start and End of Deadband #
        for end in self.deadband_ends:
            plt.axvline(x=end, color='k', linestyle='--', linewidth=0.5)
            plt.plot(end,0,'o', ms=7.5)
        for start in self.deadband_starts:
            plt.axvline(x=start, color='k', linestyle='--', linewidth=0.5)
            plt.plot(start,0,'o', ms=7.5)
        
        # Plotting Axis Labels and Sub-Plot Title #
        plt.xlabel('Time (ms)',fontsize=14)
        plt.ylabel('Response (Degrees per Second)',fontsize=14)
        plt.legend(loc='upper right', fontsize=14)
        plt.title('Measured and Ideal Response', fontsize=18)

    def __plot_cr_combined(self):
        subset = self.df[self.df['Relative Time']>=self.slope_ends['negative']]
        subset = subset[subset['Relative Time']<=self.slope_ends['positive']]

        # Only plot if slope_ends are specified #
        if len(subset) > 1:
            plt.scatter(
                subset['Wheel Input'],
                subset['Wheel Speed'], 
                label='Measured Response', 
                marker='^',
                color='tab:green',
                s=25,
                linewidths=1.75
                )
        
        plt.scatter(
            self.df[self.df['Relative Time']<= self.slope_ends['negative']]['Wheel Input'],
            self.df[self.df['Relative Time']<=self.slope_ends['negative']]['Wheel Speed'],
            label = 'Measured Response',
            color='tab:purple',
            s=50,
            marker='o',
            facecolors='none',
            linewidths=2
            )
        
        plt.scatter(
            self.df[self.df['Relative Time']<= self.slope_ends['negative']]['Wheel Input'],
            self.df[self.df['Relative Time']<=self.slope_ends['negative']]['Expected Response'],
            color = 'gray',
            s=10,
            label = 'Ideal Response'
        )
        
        # Plotting Vertical Lines Corresponding to Static and Kinetic Coefficients #
        for input in self.deadband_inputs:
            plt.axvline(x=input, color='k', linestyle='--',linewidth=0.75)
            plt.plot(input,0,'o',ms=10)
        
        # Plotting Horizontal Line to Demarkate Line for No Response Speed #
        plt.axhline(y=0, color='k',linestyle='--',linewidth=0.75)
        
        # Calculating Ticks #
        xticks = []
        set_continue = False
        step = (self.df['Wheel Input'].max()-self.df['Wheel Input'].min())/7
        for i in range(int(self.df['Wheel Input'].min()),int(self.df['Wheel Input'].max()),int(step)):
            for input in self.deadband_inputs:
                if abs(i-input) < (self.df['Wheel Input'].max()-self.df['Wheel Input'].min())/14:
                    set_continue = True
            if set_continue == True:
                set_continue = False
                continue
            else:
                xticks.append(i)
        xticks[-1] = self.df['Wheel Input'].max()
        xticks.extend(self.deadband_inputs)

        # Setting x-ticks, axese limits, axese labels and sub-plot title #
        plt.xticks(xticks)
        plt.xlim(self.df['Wheel Input'].min()/2,self.df['Wheel Input'].max()/2)
        plt.ylim([-self.df['Wheel Speed'].max()/3,self.df['Wheel Speed'].max()/3])
        plt.ylabel('Response (Degrees Per Second)', fontsize=14)
        plt.xlabel('Commanded Input (PWM Value)', fontsize=14)
        plt.legend(fontsize=14)
        plt.legend(loc='upper left',fontsize=14)
        plt.title('Commanded Input vs Response', fontsize=18)

    def __calculate_expected_output(self,pwm):
        PWM_RESOLUTION = 4095
        MOTOR_RPM = 587
        ratio = pwm/PWM_RESOLUTION
        expected_speed = (MOTOR_RPM/60)* ratio * 360
        return expected_speed

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
    starts = [59185-50300]
    ends = [62884-50300]
    inputs = [-7, 11]
    
    obj = Motor(path, starts, ends, inputs)
    obj.plot_compensation()

def plot_from_csv_rear_speed():
    path = './Python/deadband tests/deadband 8bit/SourceData/older_data/RearDeadBandDataSpeed.csv'
    starts = [16747-8175]
    ends = [20879-8175]
    inputs = [-9, 11]
    obj = Motor(path,starts,ends,inputs)
    obj.plot_compensation()

def plot_from_csv_rear_speed_triangle_unscaled():
    path = './Python/deadband tests/deadband 8bit/SourceData/older_data/TriangleRearDeadBandDataSpeed.csv'
    starts = [418599-414252, 439726-414252, 461058-414252]
    ends = [422400-414252, 443302-414252, 4.6444e+05-414252]
    inputs = [-9, 11]
    slope_ends = {'negative': 16281, 'positive': 37720}
    obj = Motor(path, starts, ends, inputs, slope_ends)
    obj.plot_compensation()

    path = './Python/deadband tests/deadband 8bit/SourceData/TriangleRearDeadBandDataSpeedUnscaled.csv'
    
    starts = [250727-240520, 271125-240520, 2.9218e+05-240520, 3.1339e+05-240520]
    ends = [253569-240520, 274913-240520, 2.9550e+05-240520, 3.1726e+05-240520]
    inputs = [-9, 11]
    slope_ends = {'negative': 21596, 'positive': 42795}
    obj = Motor(path, starts, ends, inputs, slope_ends)
    obj.plot_compensation()
    
def plot_from_csv_rear_speed_triangle_unscaled_corrected():
    path = './Python/deadband tests/deadband 8bit/SourceData/TriangleRearDeadBandDataSpeedCorrected_3.csv'
    
    obj = Motor(path, [], [], [])
    obj.plot_compensation()
    
def plot_from_csv_front_speed_triangle_unscaled():
    path = './Python/deadband tests/deadband 8bit/SourceData/TriangleFrontDeadBandDataSpeed.csv'
    starts =[376882-368002, 397929-368002, 418947-368002, 440304-368002]
    ends = [380264-368002, 401393-368002, 422848-368002, 443763-368002]
    inputs = [-11,11]
    slope_ends = {'negative': 21023, 'positive': 41849}

    obj = Motor(path,starts,ends,inputs, slope_ends)
    obj.plot_compensation()

def plot_from_csv_front_speed_triangle_unscaled_corrected():
    path = './Python/deadband tests/deadband 8bit/SourceData/TriangleFrontDeadBandDataSpeedCorrected_5.csv'

    obj = Motor(path,[],[],[])
    obj.plot_compensation()

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
    
    plot_from_csv_front()
    plot_from_csv_rear()

    plot_from_csv_front_speed()
    plot_from_csv_rear_speed()

    plot_from_csv_front_speed_triangle_unscaled()
    plot_from_csv_front_speed_triangle_unscaled_corrected()

    plot_from_csv_rear_speed_triangle_unscaled()
    plot_from_csv_rear_speed_triangle_unscaled_corrected()
