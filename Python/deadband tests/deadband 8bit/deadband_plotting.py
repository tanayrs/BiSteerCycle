'''
Experiment: Dead Band Testing
By: Jia Bhargava, Tanay Srinivasa
Last Modified: 20 June 2024

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
FRONT_COMP_PATH = 'Python/dead band/SourceData/TriangleFrontDeadBandDataSpeedCorrected_5.csv'
REAR_COMP_PATH = 'Python/dead band/SourceData/TriangleRearDeadBandDataSpeedCorrected_3.csv'

FRONT_DEADBAND_END_1 = 12253
FRONT_DEADBAND_END_2 = 33382
FRONT_DEADBAND_END_3 = 54837
FRONT_DEADBAND_END_4 = 75752
FRONT_DEADBAND_INPUT_START = -11
FRONT_DEADBAND_INPUT_END = 11

REAR_DEADBAND_END_1 = 253569 - 240536
REAR_DEADBAND_END_2 = 274913 - 240536
REAR_DEADBAND_END_3 = 2.9550e+05 - 240536
REAR_DEADBAND_END_4 = 3.1726e+05 - 240536
REAR_DEADBAND_INPUT_START = -9
REAR_DEADBAND_INPUT_END = 11

REAR_COMP_DEADBAND_END_1 = 9464
REAR_COMP_DEADBAND_END_2 = 30904
REAR_COMP_DEADBAND_END_3 = 51671

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
    axs[0].axvline(x=FRONT_DEADBAND_END_1, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=FRONT_DEADBAND_END_2, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=FRONT_DEADBAND_END_3, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=FRONT_DEADBAND_END_4, color='k', linestyle='--', linewidth=0.5)
    axs[0].axhline(y=FRONT_DEADBAND_INPUT_START, color='k', linestyle='--', linewidth=0.5)
    axs[0].axhline(y=FRONT_DEADBAND_INPUT_END, color='k', linestyle='--', linewidth=0.5)
    axs[0].plot(FRONT_DEADBAND_END_1,FRONT_DEADBAND_INPUT_START,'o')
    axs[0].plot(FRONT_DEADBAND_END_2,FRONT_DEADBAND_INPUT_END,'o')
    axs[0].plot(FRONT_DEADBAND_END_3,FRONT_DEADBAND_INPUT_START,'o')
    axs[0].plot(FRONT_DEADBAND_END_4,FRONT_DEADBAND_INPUT_END,'o')
    # axs[0].set_ylabel('Commanded Input (PWM Value)',fontsize=14)
    axs[0].set_ylabel('Input (PWM)',fontsize=28)
    axs[0].set_yticks([-50,-40,-30,-20,-11,-5,5,11,20,30,40,50])
    axs[0].set_xticks([])

    # Plot on the second axis
    axs[1].plot(df['Relative Time'], df['Front Wheel Speed'])
    axs[1].axvline(x=FRONT_DEADBAND_END_1, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=FRONT_DEADBAND_END_2, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=FRONT_DEADBAND_END_3, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=FRONT_DEADBAND_END_4, color='k', linestyle='--', linewidth=0.5)
    axs[1].plot(FRONT_DEADBAND_END_1,0,'o')
    axs[1].plot(FRONT_DEADBAND_END_2,0,'o')
    axs[1].plot(FRONT_DEADBAND_END_3,0,'o')
    axs[1].plot(FRONT_DEADBAND_END_4,0,'o')
    axs[1].set_xlabel('Time (ms)',fontsize=28)
    # axs[1].set_ylabel('Response (Degrees per Second)',fontsize=14)
    axs[1].set_ylabel('Response (d/s)',fontsize=28)

    # Show the plot
    plt.tight_layout()
    plt.show()

    sorted_df = df.sort_values('Front Wheel Input')
    plt.scatter(sorted_df['Front Wheel Input'],sorted_df['Front Wheel Speed'])
    # plt.xlabel('Commanded Value (PWM Input)', fontsize=28)
    # plt.ylabel('Response (Degrees Per Second)', fontsize=28)
    plt.xlabel('Input (PWM)', fontsize=28)
    plt.ylabel('Response (d/s)', fontsize=28)
    # plt.title('Commanded Value vs Response')
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
    axs[0].axvline(x=REAR_DEADBAND_END_1, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=REAR_DEADBAND_END_2, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=REAR_DEADBAND_END_3, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=REAR_DEADBAND_END_4, color='k', linestyle='--', linewidth=0.5)

    axs[0].plot(REAR_DEADBAND_END_1,REAR_DEADBAND_INPUT_START,'o')
    axs[0].plot(REAR_DEADBAND_END_2,REAR_DEADBAND_INPUT_END,'o')
    axs[0].plot(REAR_DEADBAND_END_3,REAR_DEADBAND_INPUT_START,'o')
    axs[0].plot(REAR_DEADBAND_END_4,REAR_DEADBAND_INPUT_END,'o')

    axs[0].axhline(y=REAR_DEADBAND_INPUT_START, color='k', linestyle='--', linewidth=0.5)
    axs[0].axhline(y=REAR_DEADBAND_INPUT_END, color='k', linestyle='--', linewidth=0.5)
    axs[0].set_ylabel('Commanded Input (PWM Value)',fontsize=14)
    axs[0].set_yticks([-50,-40,-30,-20,-9,-5,5,11,20,30,40,50])
    axs[0].set_xticks([])

    # Plot on the second axis
    axs[1].plot(df['Relative Time'], df['Rear Wheel Speed'])
    axs[1].axvline(x=REAR_DEADBAND_END_1, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=REAR_DEADBAND_END_2, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=REAR_DEADBAND_END_3, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=REAR_DEADBAND_END_4, color='k', linestyle='--', linewidth=0.5)

    axs[1].plot(REAR_DEADBAND_END_1,0,'o')
    axs[1].plot(REAR_DEADBAND_END_2,0,'o')
    axs[1].plot(REAR_DEADBAND_END_3,0,'o')
    axs[1].plot(REAR_DEADBAND_END_4,0,'o')

    axs[1].set_xlabel('Time (ms)',fontsize=14)
    axs[1].set_ylabel('Response (Degrees per Second)',fontsize=14)

    # Show the plot
    plt.tight_layout()
    plt.show()

    sorted_df = df.sort_values('Rear Wheel Input')
    plt.scatter(sorted_df['Rear Wheel Input'],sorted_df['Rear Wheel Speed'])
    plt.xlabel('Commanded Value (PWM Input)')
    plt.ylabel('Response (Degrees Per Second)')
    plt.title('Commanded Value vs Response')
    plt.show()

def plot_front_compensated():
    path = 'Python/dead band/SourceData/TriangleFrontDeadBandDataSpeedCorrected_5.csv'
    ends = [12840, 34054, 55066, 76309]
    FRONT_COMP_DEADBAND_END_1 = 12840
    FRONT_COMP_DEADBAND_END_2 = 34054
    FRONT_COMP_DEADBAND_END_3 = 55066
    FRONT_COMP_DEADBAND_END_4 = 76309
    # Reading CSV into pandas DataFrame #
    df = pd.read_csv(FRONT_COMP_PATH)
    df['Relative Time'] = df['Time']-df['Time'].iloc[0]

    # Plotting Angle vs Time #
    fig, axs = plt.subplots(2, 1)
    fig.set_figheight(8.5)
    fig.set_figwidth(14)

    # Plot on the first axis
    axs[0].plot(df['Relative Time'], df['Front Wheel Input'])
    axs[0].axvline(x=FRONT_COMP_DEADBAND_END_1, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=FRONT_COMP_DEADBAND_END_2, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=FRONT_COMP_DEADBAND_END_3, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=FRONT_COMP_DEADBAND_END_4, color='k', linestyle='--', linewidth=0.5)
    axs[0].axhline(y=FRONT_DEADBAND_INPUT_START, color='k', linestyle='--', linewidth=0.5)
    axs[0].axhline(y=FRONT_DEADBAND_INPUT_END, color='k', linestyle='--', linewidth=0.5)
    axs[0].plot(FRONT_COMP_DEADBAND_END_1,FRONT_DEADBAND_INPUT_END,'o')
    axs[0].plot(FRONT_COMP_DEADBAND_END_2,FRONT_DEADBAND_INPUT_START,'o')
    axs[0].plot(FRONT_COMP_DEADBAND_END_3,FRONT_DEADBAND_INPUT_END,'o')
    axs[0].plot(FRONT_COMP_DEADBAND_END_4,FRONT_DEADBAND_INPUT_START,'o')
    axs[0].set_ylabel('Commanded Input (PWM Value)',fontsize=14)
    axs[0].set_yticks([-50,-40,-30,-20,-11,-5,5,11,20,30,40,50])
    axs[0].set_xticks([])
    # axs[0].set_title('Commanded Input vs Time')

    # Plot on the second axis
    axs[1].plot(df['Relative Time'], df['Front Wheel Speed'])
    axs[1].axvline(x=FRONT_COMP_DEADBAND_END_1, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=FRONT_COMP_DEADBAND_END_2, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=FRONT_COMP_DEADBAND_END_3, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=FRONT_COMP_DEADBAND_END_4, color='k', linestyle='--', linewidth=0.5)
    axs[1].plot(FRONT_COMP_DEADBAND_END_1,0,'o')
    axs[1].plot(FRONT_COMP_DEADBAND_END_2,0,'o')
    axs[1].plot(FRONT_COMP_DEADBAND_END_3,0,'o')
    axs[1].plot(FRONT_COMP_DEADBAND_END_4,0,'o')
    axs[1].set_xlabel('Time (ms)',fontsize=14)
    axs[1].set_ylabel('Response (Degrees per Second)',fontsize=14)
    # axs[1].set_title('Response vs Time')

    # Show the plot
    plt.tight_layout()
    plt.show()

    sorted_df = df.sort_values('Front Wheel Input')
    plt.scatter(sorted_df['Front Wheel Input'],sorted_df['Front Wheel Speed'])
    plt.xlabel('Commanded Value (PWM Input)')
    plt.ylabel('Response (Degrees Per Second)')
    plt.title('Commanded Value vs Response')
    plt.show()

def plot_rear_compensated():
    # Reading CSV into pandas DataFrame #
    df = pd.read_csv(REAR_COMP_PATH)
    df['Relative Time'] = df['Time']-df['Time'].iloc[0]

    # Plotting Angle vs Time #
    fig, axs = plt.subplots(2, 1)
    fig.set_figheight(8.5)
    fig.set_figwidth(14)

    # Plot on the first axis
    axs[0].plot(df['Relative Time'], df['Rear Wheel Input'])
    axs[0].axvline(x=REAR_COMP_DEADBAND_END_1, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=REAR_COMP_DEADBAND_END_2, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=REAR_COMP_DEADBAND_END_3, color='k', linestyle='--', linewidth=0.5)
    axs[0].axhline(y=REAR_DEADBAND_INPUT_START, color='k', linestyle='--', linewidth=0.5)
    axs[0].axhline(y=REAR_DEADBAND_INPUT_END, color='k', linestyle='--', linewidth=0.5)
    axs[0].plot(REAR_COMP_DEADBAND_END_1,REAR_DEADBAND_INPUT_START,'o')
    axs[0].plot(REAR_COMP_DEADBAND_END_2,REAR_DEADBAND_INPUT_END,'o')
    axs[0].plot(REAR_COMP_DEADBAND_END_3,REAR_DEADBAND_INPUT_START,'o')
    axs[0].set_ylabel('Commanded Input (PWM Value)',fontsize=14)
    axs[0].set_yticks([-50,-40,-30,-20,REAR_DEADBAND_INPUT_START,-5,5,REAR_DEADBAND_INPUT_END,20,30,40,50])
    axs[0].set_xticks([])

    # Plot on the second axis
    axs[1].plot(df['Relative Time'], df['Rear Wheel Speed'])
    axs[1].axvline(x=REAR_COMP_DEADBAND_END_1, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=REAR_COMP_DEADBAND_END_2, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=REAR_COMP_DEADBAND_END_3, color='k', linestyle='--', linewidth=0.5)
    axs[1].plot(REAR_COMP_DEADBAND_END_1,0,'o')
    axs[1].plot(REAR_COMP_DEADBAND_END_2,0,'o')
    axs[1].plot(REAR_COMP_DEADBAND_END_3,0,'o')
    axs[1].set_xlabel('Time (ms)',fontsize=14)
    axs[1].set_ylabel('Response (Degrees per Second)',fontsize=14)

    # Show the plot
    plt.tight_layout()
    plt.show()

    sorted_df = df.sort_values('Rear Wheel Input')
    plt.scatter(sorted_df['Rear Wheel Input'],sorted_df['Rear Wheel Speed'])
    plt.xlabel('Commanded Value (PWM Input)')
    plt.ylabel('Response (Degrees Per Second)')
    plt.title('Commanded Value vs Response')
    plt.show()

if __name__ == '__main__':
    plot_front()
    # plot_rear()
    # plot_front_compensated()
    # plot_rear_compensated()