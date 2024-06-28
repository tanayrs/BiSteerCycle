'''
Experiment: Dead Band Testing with 12bit PWM Resolution
By: Jia Bhargava, Tanay Srinivasa
Last Modified: 24 June 2024

Run bi_steer_cycle_testing arduino code with deadband_test()
'''

import serial
import time
import csv
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

FRONT_PATH = './Python/deadband 12bit/SourceData/FrontUncompensatedData.csv'
REAR_PATH = './Python/deadband 12bit/SourceData/RearUncompensatedData.csv'
FRONT_COMP_PATH = './Python/deadband 12bit/SourceData/FrontCompensatedData.csv'
REAR_COMP_PATH = './Python/deadband 12bit/SourceData/RearCompensatedData.csv'

FRONT_DEADBAND_END_1 = 8174
FRONT_DEADBAND_END_2 = 26449
FRONT_DEADBAND_END_3 = 43525
FRONT_DEADBAND_END_4 = 61378
FRONT_DEADBAND_INPUT_START = -170
FRONT_DEADBAND_INPUT_END = 215

REAR_DEADBAND_END_1 = 10279
REAR_DEADBAND_END_2 = 27891
REAR_DEADBAND_END_3 = 45383
REAR_DEADBAND_END_4 = 62937
REAR_DEADBAND_INPUT_START = -160
REAR_DEADBAND_INPUT_END = 170

FRONT_COMP_DEADBAND_END_1 = 10526
FRONT_COMP_DEADBAND_END_2 = 28583
FRONT_COMP_DEADBAND_END_3 = 45684
FRONT_COMP_DEADBAND_END_4 = 63689

REAR_COMP_DEADBAND_END_1 = 10520
REAR_COMP_DEADBAND_END_2 = 28132
REAR_COMP_DEADBAND_END_3 = 45625
REAR_COMP_DEADBAND_END_4 = 63293

def plot_front():
    # Reading CSV into pandas DataFrame #
    df = pd.read_csv(FRONT_PATH)
    df['Relative Time'] = df['Time']-df['Time'].iloc[0]
    print(df['Time'].iloc[0])

    # Plotting Angle vs Time #
    fig, axs = plt.subplots(2, 1)
    fig.set_figheight(8.5)
    fig.set_figwidth(14)

    # Plot on the first axis
    axs[0].plot(df['Relative Time'], df['Wheel Input'])
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
    axs[0].set_ylabel('Commanded Input (PWM Value)',fontsize=14)
    axs[0].set_yticks([-800,-600,-400,-170,0,215,400,600,800])
    axs[0].set_xticks([])

    # Plot on the second axis
    axs[1].plot(df['Relative Time'], df['Wheel Speed'])
    axs[1].axvline(x=FRONT_DEADBAND_END_1, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=FRONT_DEADBAND_END_2, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=FRONT_DEADBAND_END_3, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=FRONT_DEADBAND_END_4, color='k', linestyle='--', linewidth=0.5)
    axs[1].plot(FRONT_DEADBAND_END_1,0,'o')
    axs[1].plot(FRONT_DEADBAND_END_2,0,'o')
    axs[1].plot(FRONT_DEADBAND_END_3,0,'o')
    axs[1].plot(FRONT_DEADBAND_END_4,0,'o')
    axs[1].set_xlabel('Time (ms)',fontsize=14)
    axs[1].set_ylabel('Response (Degrees per Second)',fontsize=14)

    # Show the plot
    plt.tight_layout()
    plt.show()

    sorted_df = df.sort_values('Wheel Input')
    plt.scatter(sorted_df['Wheel Input'],sorted_df['Wheel Speed'])
    plt.vlines(x=FRONT_DEADBAND_INPUT_START, ymin= -80,ymax=0, color='k', linestyle='--',linewidth=0.75)
    plt.vlines(x=FRONT_DEADBAND_INPUT_END, ymin= -80,ymax=0, color='k', linestyle='--',linewidth=0.75)
    plt.axhline(y=0, color='k', linestyle='--',linewidth=0.75)
    plt.plot(FRONT_DEADBAND_INPUT_START, 0, 'o', color='tab:red')
    plt.plot(FRONT_DEADBAND_INPUT_END, 0, 'o', color='tab:orange')
    plt.xticks([-800,-600,-400,FRONT_DEADBAND_INPUT_START, 0, FRONT_DEADBAND_INPUT_END, 400, 600, 800])
    plt.xlabel('Commanded Value (PWM Input)', fontsize=14)
    plt.ylabel('Response (Degrees Per Second)', fontsize=14)
    plt.title('Commanded Value vs Response', fontsize=14)
    plt.show()

def plot_rear():
    # Reading CSV into pandas DataFrame #
    df = pd.read_csv(REAR_PATH)
    df['Relative Time'] = df['Time']-df['Time'].iloc[0]
    print(df['Time'].iloc[0])

    # Plotting Angle vs Time #
    fig, axs = plt.subplots(2, 1)
    fig.set_figheight(8.5)
    fig.set_figwidth(14)

    # Plot on the first axis
    axs[0].plot(df['Relative Time'], df['Wheel Input'])
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
    axs[0].set_yticks([-800,-600,-400,-160,0,170,400,600,800])
    axs[0].set_xticks([])

    # Plot on the second axis
    axs[1].plot(df['Relative Time'], df['Wheel Speed'])
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

    sorted_df = df.sort_values('Wheel Input')
    plt.scatter(sorted_df['Wheel Input'],sorted_df['Wheel Speed'])
    plt.vlines(x=REAR_DEADBAND_INPUT_START, ymin= -80,ymax=0, color='k', linestyle='--',linewidth=0.75)
    plt.vlines(x=REAR_DEADBAND_INPUT_END, ymin= -80,ymax=0, color='k', linestyle='--',linewidth=0.75)
    plt.axhline(y=0, color='k', linestyle='--',linewidth=0.75)
    plt.plot(REAR_DEADBAND_INPUT_START, 0, 'o', color='tab:red')
    plt.plot(REAR_DEADBAND_INPUT_END, 0, 'o', color='tab:orange')
    plt.xticks([-800,-600,-400,REAR_DEADBAND_INPUT_START, 0, REAR_DEADBAND_INPUT_END, 400, 600, 800])
    plt.xlabel('Commanded Value (PWM Input)', fontsize=14)
    plt.ylabel('Response (Degrees Per Second)', fontsize=14)
    plt.title('Commanded Value vs Response', fontsize=14)
    plt.show()

def plot_front_compensated():
    # Reading CSV into pandas DataFrame #
    df = pd.read_csv(FRONT_COMP_PATH)
    df['Relative Time'] = df['Time']-df['Time'].iloc[0]
    print(df['Time'].iloc[0])

    # Plotting Angle vs Time #
    fig, axs = plt.subplots(2, 1)
    fig.set_figheight(8.5)
    fig.set_figwidth(14)

    # Plot on the first axis
    axs[0].plot(df['Relative Time'], df['Wheel Input'])
    axs[0].axvline(x=FRONT_COMP_DEADBAND_END_1, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=FRONT_COMP_DEADBAND_END_2, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=FRONT_COMP_DEADBAND_END_3, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=FRONT_COMP_DEADBAND_END_4, color='k', linestyle='--', linewidth=0.5)
    
    axs[0].axhline(y=FRONT_DEADBAND_INPUT_START, color='k', linestyle='--', linewidth=0.5)
    axs[0].axhline(y=FRONT_DEADBAND_INPUT_END, color='k', linestyle='--', linewidth=0.5)
    
    axs[0].plot(FRONT_COMP_DEADBAND_END_1,FRONT_DEADBAND_INPUT_START,'o')
    axs[0].plot(FRONT_COMP_DEADBAND_END_2,FRONT_DEADBAND_INPUT_END,'o')
    axs[0].plot(FRONT_COMP_DEADBAND_END_3,FRONT_DEADBAND_INPUT_START,'o')
    axs[0].plot(FRONT_COMP_DEADBAND_END_4,FRONT_DEADBAND_INPUT_END,'o')
    
    axs[0].set_ylabel('Commanded Input (PWM Value)',fontsize=14)
    axs[0].set_yticks([-800,-600,-400,-170,0,215,400,600,800])
    axs[0].set_xticks([])
    # axs[0].set_title('Commanded Input vs Time')

    # Plot on the second axis
    axs[1].plot(df['Relative Time'], df['Wheel Speed'])
    axs[1].axvline(x=FRONT_COMP_DEADBAND_END_1, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=FRONT_COMP_DEADBAND_END_2, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=FRONT_COMP_DEADBAND_END_3, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=FRONT_COMP_DEADBAND_END_4, color='k', linestyle='--', linewidth=0.5)
    axs[1].axhline(y=0, color='k', linestyle='--', linewidth=0.5)
    axs[1].set_xlabel('Time (ms)',fontsize=14)
    axs[1].set_ylabel('Response (Degrees per Second)',fontsize=14)

    # Show the plot
    plt.tight_layout()
    plt.show()

    sorted_df = df.sort_values('Wheel Input')
    plt.scatter(sorted_df['Wheel Input'],sorted_df['Wheel Speed'])
    plt.axvline(x=FRONT_DEADBAND_INPUT_START, color='k', linestyle='--',linewidth=0.75)
    plt.axvline(x=FRONT_DEADBAND_INPUT_END, color='k', linestyle='--',linewidth=0.75)
    plt.axhline(y=0, color='k', linestyle='--',linewidth=0.75)
    # plt.plot(FRONT_DEADBAND_INPUT_START, -19, 'o', color='tab:red')
    # plt.plot(FRONT_DEADBAND_INPUT_END, 24.7, 'o', color='tab:orange')
    plt.plot(FRONT_DEADBAND_INPUT_START, 0, 'o', color='tab:red')
    plt.plot(FRONT_DEADBAND_INPUT_END, 0, 'o', color='tab:orange')
    plt.xticks([-800,-600,-400,FRONT_DEADBAND_INPUT_START, 0, FRONT_DEADBAND_INPUT_END, 400, 600, 800])
    plt.xlabel('Commanded Value (PWM Input)', fontsize=14)
    plt.ylabel('Response (Degrees Per Second)', fontsize=14)
    plt.title('Commanded Value vs Response', fontsize=14)
    plt.show()

def plot_rear_compensated():
    # Reading CSV into pandas DataFrame #
    df = pd.read_csv(REAR_COMP_PATH)
    df['Relative Time'] = df['Time']-df['Time'].iloc[0]
    print(df['Time'].iloc[0])

    # Plotting Angle vs Time #
    fig, axs = plt.subplots(2, 1)
    fig.set_figheight(8.5)
    fig.set_figwidth(14)

    # Plot on the first axis
    axs[0].plot(df['Relative Time'], df['Wheel Input'])
    
    axs[0].axvline(x=REAR_COMP_DEADBAND_END_1, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=REAR_COMP_DEADBAND_END_2, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=REAR_COMP_DEADBAND_END_3, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=REAR_COMP_DEADBAND_END_4, color='k', linestyle='--', linewidth=0.5)
    
    axs[0].axhline(y=REAR_DEADBAND_INPUT_START, color='k', linestyle='--', linewidth=0.5)
    axs[0].axhline(y=REAR_DEADBAND_INPUT_END, color='k', linestyle='--', linewidth=0.5)
    
    axs[0].plot(REAR_COMP_DEADBAND_END_1,REAR_DEADBAND_INPUT_START,'o')
    axs[0].plot(REAR_COMP_DEADBAND_END_2,REAR_DEADBAND_INPUT_END,'o')
    axs[0].plot(REAR_COMP_DEADBAND_END_3,REAR_DEADBAND_INPUT_START,'o')
    axs[0].plot(REAR_COMP_DEADBAND_END_4,REAR_DEADBAND_INPUT_END,'o')
    
    axs[0].set_ylabel('Commanded Input (PWM Value)',fontsize=14)
    axs[0].set_yticks([-800,-600,-400,-160,0,170,400,600,800])
    axs[0].set_xticks([])

    # Plot on the second axis
    axs[1].plot(df['Relative Time'], df['Wheel Speed'])
    axs[1].axvline(x=REAR_COMP_DEADBAND_END_1, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=REAR_COMP_DEADBAND_END_2, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=REAR_COMP_DEADBAND_END_3, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=REAR_COMP_DEADBAND_END_4, color='k', linestyle='--', linewidth=0.5)
    axs[1].axhline(y=0, color='k', linestyle='--', linewidth=0.5)
    # axs[1].plot(REAR_COMP_DEADBAND_END_1,0,'o')
    # axs[1].plot(REAR_COMP_DEADBAND_END_2,0,'o')
    # axs[1].plot(REAR_COMP_DEADBAND_END_3,0,'o')
    # axs[1].plot(REAR_COMP_DEADBAND_END_4,0,'o')
    axs[1].set_xlabel('Time (ms)',fontsize=14)
    axs[1].set_ylabel('Response (Degrees per Second)',fontsize=14)

    # Show the plot
    plt.tight_layout()
    plt.show()

    sorted_df = df.sort_values('Wheel Input')
    plt.scatter(sorted_df['Wheel Input'],sorted_df['Wheel Speed'])
    plt.axvline(x=REAR_DEADBAND_INPUT_START, color='k', linestyle='--',linewidth=0.75)
    plt.axvline(x=REAR_DEADBAND_INPUT_END, color='k', linestyle='--',linewidth=0.75)
    plt.axhline(y=0, color='k', linestyle='--',linewidth=0.75)
    plt.plot(REAR_DEADBAND_INPUT_START, 0, 'o', color='tab:red')
    plt.plot(REAR_DEADBAND_INPUT_END, 0, 'o', color='tab:orange')
    plt.xticks([-800,-600,-400,REAR_DEADBAND_INPUT_START, 0, REAR_DEADBAND_INPUT_END, 400, 600, 800])
    plt.xlabel('Commanded Value (PWM Input)', fontsize=14)
    plt.ylabel('Response (Degrees Per Second)', fontsize=14)
    plt.title('Commanded Value vs Response', fontsize=14)
    plt.show()

if __name__ == '__main__':
    # plot_front()
    # plot_rear()
    # plot_front_compensated()
    plot_rear_compensated()