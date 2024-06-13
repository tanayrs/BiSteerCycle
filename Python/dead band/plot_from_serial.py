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

REAR_PATH = './Python/dead band/RearDeadBandData.csv'
FRONT_PATH = './Python/dead band/FrontDeadBandData.csv'
FRONT_SPEED_PATH = './Python/dead band/FrontDeadBandDataSpeed.csv'
REAR_SPEED_PATH = './Python/dead band/RearDeadBandDataSpeed.csv'
COM = '/dev/cu.usbmodem160464801'
BAUD = 115200

REAR_TIME_DEADBAND_START = 16752
REAR_TIME_DEADBAND_END = 20690
REAR_SPEED_DEADBAND_START = -8
REAR_SPEED_DEADBAND_END = 12

FRONT_TIME_DEADBAND_START = 36762
FRONT_TIME_DEADBAND_END = 41905
FRONT_SPEED_DEADBAND_START = -10
FRONT_SPEED_DEADBAND_END = 15

FRONT_SPEED_TIME_DEADBAND_START = 59185
FRONT_SPEED_TIME_DEADBAND_END = 62884
FRONT_SPEED_DEADBAND_START = -7
FRONT_SPEED_DEADBAND_END = 11

REAR_SPEED_TIME_DEADBAND_START = 16747
REAR_SPEED_TIME_DEADBAND_END = 20879
REAR_SPEED_DEADBAND_START = -9
REAR_SPEED_DEADBAND_END = 11

# Plotting Sensor Value Readings #
def plot_from_csv_rear():
    # Reading CSV into pandas DataFrame #
    df = pd.read_csv(REAR_PATH)

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

# Plotting Sensor Value Readings #
def plot_from_csv_front():
    # Reading CSV into pandas DataFrame #
    df = pd.read_csv(FRONT_PATH)

    # Printing Statistics of DataFrame #
    print(df.describe())

    # Plotting Angle vs Time #
    fig, axs = plt.subplots(2, 1)
    fig.set_figheight(10)
    fig.set_figwidth(12)

    # Plot on the first axis
    axs[0].plot(df['Time'], df['Front Wheel Input'])
    axs[0].axvline(x=FRONT_TIME_DEADBAND_START, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=FRONT_TIME_DEADBAND_END, color='k', linestyle='--', linewidth=0.5)
    axs[0].axhline(y=FRONT_SPEED_DEADBAND_START, color='k', linestyle='--', linewidth=0.5)
    axs[0].axhline(y=FRONT_SPEED_DEADBAND_END, color='k', linestyle='--', linewidth=0.5)
    axs[0].set_xlabel('Time')
    axs[0].set_ylabel('Input Speed')
    axs[0].set_yticks(np.arange(-50,50,step=5))

    # Plot on the second axis
    axs[1].plot(df['Time'], df['Front Wheel Ticks'])
    axs[1].axvline(x=FRONT_TIME_DEADBAND_START, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=FRONT_TIME_DEADBAND_END, color='k', linestyle='--', linewidth=0.5)
    axs[1].set_xlabel('Time')
    axs[1].set_ylabel('Encoder Ticks')

    # Show the plot
    plt.show()

def plot_from_csv_front_speed():
    # Reading CSV into pandas DataFrame #
    df = pd.read_csv(FRONT_SPEED_PATH)

    # Printing Statistics of DataFrame #
    print(df.describe())

    # Plotting Angle vs Time #
    fig, axs = plt.subplots(2, 1)
    fig.set_figheight(10)
    fig.set_figwidth(12)

    # Plot on the first axis
    axs[0].plot(df['Time'], df['Front Wheel Input'])
    axs[0].axvline(x=FRONT_SPEED_TIME_DEADBAND_START, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=FRONT_SPEED_TIME_DEADBAND_END, color='k', linestyle='--', linewidth=0.5)
    axs[0].axhline(y=FRONT_SPEED_DEADBAND_START, color='k', linestyle='--', linewidth=0.5)
    axs[0].axhline(y=FRONT_SPEED_DEADBAND_END, color='k', linestyle='--', linewidth=0.5)
    axs[0].set_ylabel('Input Speed (PWM Value)',fontsize=14)
    axs[0].set_yticks([-50,-40,-30,-20,-10,-5,0,5,10,20,30,40,50])
    axs[0].set_xticks([])

    # Plot on the second axis
    axs[1].plot(df['Time'], df['Front Wheel Speed'])
    axs[1].axvline(x=FRONT_SPEED_TIME_DEADBAND_START, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=FRONT_SPEED_TIME_DEADBAND_END, color='k', linestyle='--', linewidth=0.5)
    axs[1].set_xlabel('Time (ms)',fontsize=14)
    axs[1].set_ylabel('Encoder Speed (Degrees per Second)',fontsize=14)

    # Show the plot
    plt.tight_layout()
    plt.show()

def plot_from_csv_rear_speed():
    # Reading CSV into pandas DataFrame #
    df = pd.read_csv(REAR_SPEED_PATH)

    # Printing Statistics of DataFrame #
    print(df.describe())

    # Plotting Angle vs Time #
    fig, axs = plt.subplots(2, 1)
    fig.set_figheight(10)
    fig.set_figwidth(12)

    # Plot on the first axis
    axs[0].plot(df['Time'], df['Rear Wheel Input'])
    axs[0].axvline(x=REAR_SPEED_TIME_DEADBAND_START, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=REAR_SPEED_TIME_DEADBAND_END, color='k', linestyle='--', linewidth=0.5)
    axs[0].axhline(y=REAR_SPEED_DEADBAND_START, color='k', linestyle='--', linewidth=0.5)
    axs[0].axhline(y=REAR_SPEED_DEADBAND_END, color='k', linestyle='--', linewidth=0.5)
    axs[0].set_ylabel('Input Speed (PWM Value)',fontsize=14)
    axs[0].set_yticks([-50,-40,-30,-20,-10,-5,5,10,20,30,40,50])
    axs[0].set_xticks([])

    # Plot on the second axis
    axs[1].plot(df['Time'], df['Rear Wheel Speed'])
    axs[1].axvline(x=REAR_SPEED_TIME_DEADBAND_START, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=REAR_SPEED_TIME_DEADBAND_END, color='k', linestyle='--', linewidth=0.5)
    axs[1].set_xlabel('Time (ms)',fontsize=14)
    axs[1].set_ylabel('Encoder Speed (Degrees per Second)',fontsize=14)

    # Show the plot
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # read_from_serial_rear()
    # plot_from_csv_rear()
    # read_from_serial_front()
    # plot_from_csv_front()
    plot_from_csv_front_speed()
    # plot_from_csv_rear_speed()