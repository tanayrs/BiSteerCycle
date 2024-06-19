'''
Experiment: Dead Band Testing
By: Jia Bhargava, Tanay Srinivasa
Last Modified: 19 June 2024

Run bi_steer_cycle arduino code with set_dead_band_speed()
'''

import serial
import time
import csv
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

FRONT_PATH = './Python/dead band/SourceData/TriangleFrontDeadBandDataSpeed.csv'
REAR_PATH = './Python/dead band/SourceData/TriangleRearDeadBandDataSpeedUnscaled.csv'

REAR_TIME_DEADBAND_END_1 = 422400
REAR_TIME_DEADBAND_END_2 = 443302
REAR_TIME_DEADBAND_END_3 = 4.6444e+05
REAR_DEADBAND_START = -9
REAR_DEADBAND_END = 11

REAR_TIME_DEADBAND_END_UNSCALED_1 = 253569 - 245425 
REAR_TIME_DEADBAND_END_UNSCALED_2 = 274913 - 245425 
REAR_TIME_DEADBAND_END_UNSCALED_3 = 2.9550e+05 - 245425 
REAR_TIME_DEADBAND_END_UNSCALED_4 = 3.1726e+05 - 245425 
REAR_DEADBAND_UNSCALED_START = -9
REAR_DEADBAND_UNSCALED_END = 11

FRONT_TIME_DEADBAND_END_UNSCALED_1 = 12253
FRONT_TIME_DEADBAND_END_UNSCALED_2 = 33382
FRONT_TIME_DEADBAND_END_UNSCALED_3 = 54837
FRONT_TIME_DEADBAND_END_UNSCALED_4 = 75752
FRONT_DEADBAND_UNSCALED_START = -11
FRONT_DEADBAND_UNSCALED_END = 11

def plot_front():
    # Reading CSV into pandas DataFrame #
    df = pd.read_csv(FRONT_PATH)
    df['Relative Time'] = df['Time']-df['Time'].iloc[0]

    # Plotting Angle vs Time #
    fig, axs = plt.subplots(2, 1)
    fig.set_figheight(8.5)
    fig.set_figwidth(14)

    # Plot on the first axis
    axs[0].plot(df['Relative Time'], df['Front Wheel Input'])
    axs[0].axvline(x=FRONT_TIME_DEADBAND_END_UNSCALED_1, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=FRONT_TIME_DEADBAND_END_UNSCALED_2, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=FRONT_TIME_DEADBAND_END_UNSCALED_3, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=FRONT_TIME_DEADBAND_END_UNSCALED_4, color='k', linestyle='--', linewidth=0.5)
    axs[0].axhline(y=FRONT_DEADBAND_UNSCALED_START, color='k', linestyle='--', linewidth=0.5)
    axs[0].axhline(y=FRONT_DEADBAND_UNSCALED_END, color='k', linestyle='--', linewidth=0.5)
    axs[0].plot(FRONT_TIME_DEADBAND_END_UNSCALED_1,FRONT_DEADBAND_UNSCALED_START,'o')
    axs[0].plot(FRONT_TIME_DEADBAND_END_UNSCALED_2,FRONT_DEADBAND_UNSCALED_END,'o')
    axs[0].plot(FRONT_TIME_DEADBAND_END_UNSCALED_3,FRONT_DEADBAND_UNSCALED_START,'o')
    axs[0].plot(FRONT_TIME_DEADBAND_END_UNSCALED_4,FRONT_DEADBAND_UNSCALED_END,'o')
    axs[0].set_ylabel('Commanded Input (PWM Value)',fontsize=14)
    axs[0].set_yticks([-50,-40,-30,-20,-11,-5,5,11,20,30,40,50])
    axs[0].set_xticks([])

    # Plot on the second axis
    axs[1].plot(df['Relative Time'], df['Front Wheel Speed'])
    axs[1].axvline(x=FRONT_TIME_DEADBAND_END_UNSCALED_1, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=FRONT_TIME_DEADBAND_END_UNSCALED_2, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=FRONT_TIME_DEADBAND_END_UNSCALED_3, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=FRONT_TIME_DEADBAND_END_UNSCALED_4, color='k', linestyle='--', linewidth=0.5)
    axs[1].plot(FRONT_TIME_DEADBAND_END_UNSCALED_1,0,'o')
    axs[1].plot(FRONT_TIME_DEADBAND_END_UNSCALED_2,0,'o')
    axs[1].plot(FRONT_TIME_DEADBAND_END_UNSCALED_3,0,'o')
    axs[1].plot(FRONT_TIME_DEADBAND_END_UNSCALED_4,0,'o')
    axs[1].set_xlabel('Time (ms)',fontsize=14)
    axs[1].set_ylabel('Response (Degrees per Second)',fontsize=14)

    # Show the plot
    plt.tight_layout()
    plt.show()

    sorted_df = df.sort_values('Front Wheel Input')
    plt.scatter(sorted_df['Front Wheel Input'],sorted_df['Front Wheel Speed'])
    plt.xlabel('Commanded Value (PWM Input)')
    plt.ylabel('Response (Degrees Per Second)')
    plt.title('Commanded Value vs Response')
    plt.show()

def plot_rear():
    # Reading CSV into pandas DataFrame #
    df = pd.read_csv(REAR_PATH)
    df['Relative Time'] = df['Time']-df['Time'].iloc[0]

    # Plotting Angle vs Time #
    fig, axs = plt.subplots(2, 1)
    fig.set_figheight(8.5)
    fig.set_figwidth(14)

    # Plot on the first axis
    axs[0].plot(df['Relative Time'], df['Rear Wheel Input'])
    axs[0].axvline(x=REAR_TIME_DEADBAND_END_UNSCALED_1, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=REAR_TIME_DEADBAND_END_UNSCALED_2, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=REAR_TIME_DEADBAND_END_UNSCALED_3, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=REAR_TIME_DEADBAND_END_UNSCALED_4, color='k', linestyle='--', linewidth=0.5)

    axs[0].plot(REAR_TIME_DEADBAND_END_UNSCALED_1,REAR_DEADBAND_START,'o')
    axs[0].plot(REAR_TIME_DEADBAND_END_UNSCALED_2,REAR_DEADBAND_END,'o')
    axs[0].plot(REAR_TIME_DEADBAND_END_UNSCALED_3,REAR_DEADBAND_START,'o')
    axs[0].plot(REAR_TIME_DEADBAND_END_UNSCALED_4,REAR_DEADBAND_END,'o')

    axs[0].axhline(y=REAR_DEADBAND_START, color='k', linestyle='--', linewidth=0.5)
    axs[0].axhline(y=REAR_DEADBAND_END, color='k', linestyle='--', linewidth=0.5)
    axs[0].set_ylabel('Input Speed (PWM Value)',fontsize=14)
    axs[0].set_yticks([-50,-40,-30,-20,-10,-5,5,10,20,30,40,50])
    axs[0].set_xticks([])

    # Plot on the second axis
    axs[1].plot(df['Relative Time'], df['Rear Wheel Speed'])
    axs[1].axvline(x=REAR_TIME_DEADBAND_END_UNSCALED_1, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=REAR_TIME_DEADBAND_END_UNSCALED_2, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=REAR_TIME_DEADBAND_END_UNSCALED_3, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=REAR_TIME_DEADBAND_END_UNSCALED_4, color='k', linestyle='--', linewidth=0.5)

    axs[1].plot(REAR_TIME_DEADBAND_END_UNSCALED_1,0,'o')
    axs[1].plot(REAR_TIME_DEADBAND_END_UNSCALED_2,0,'o')
    axs[1].plot(REAR_TIME_DEADBAND_END_UNSCALED_3,0,'o')
    axs[1].plot(REAR_TIME_DEADBAND_END_UNSCALED_4,0,'o')

    axs[1].set_xlabel('Time (ms)',fontsize=14)
    axs[1].set_ylabel('Encoder Speed (Degrees per Second)',fontsize=14)

    # Show the plot
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # plot_front()
    plot_rear()