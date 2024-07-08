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
REAR_COMP_PATH = './Python/deadband 12bit/SourceData/RearOverCompensatedData.csv'

FRONT_DEADBAND_END_1 = 8174
FRONT_DEADBAND_END_2 = 26449
FRONT_DEADBAND_END_3 = 43525
FRONT_DEADBAND_END_4 = 61378
FRONT_DEADBAND_START_1 = 5066
FRONT_DEADBAND_START_2 = 22488
FRONT_DEADBAND_START_3 = 40158
FRONT_DEADBAND_START_4 = 57770

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

KINETIC_COEFF_DEC = 130
KINETIC_COEFF_INC = -135
STATIC_COEFF_INC = FRONT_DEADBAND_INPUT_END
STATIC_COEFF_DEC = FRONT_DEADBAND_INPUT_START

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

def command_response_front():
    df = pd.read_csv(FRONT_PATH)
    df['Relative Time'] = df['Time'] - df['Time'].iloc[0]
    df['Wheel Speed Corrected'] = df['Wheel Speed']*8

    plt.figure(figsize=(14,8.5))
    
    ### Command vs Time Plot ###
    plt.subplot(2,2,1)
    real_effective_input(df)
    # plt.plot(df['Relative Time'], df['Wheel Input'])
    
    # # Plotting Vertical Lines at Times where deadband is entered and exitted #
    # plt.vlines(x=FRONT_DEADBAND_END_1, ymin=-900, ymax=STATIC_COEFF_DEC, color='k', linestyle='--', linewidth=0.5)
    # plt.vlines(x=FRONT_DEADBAND_END_2, ymin=-900, ymax=STATIC_COEFF_INC, color='k', linestyle='--', linewidth=0.5)
    # plt.vlines(x=FRONT_DEADBAND_END_3, ymin=-900, ymax=STATIC_COEFF_DEC, color='k', linestyle='--', linewidth=0.5)
    # plt.vlines(x=FRONT_DEADBAND_END_4, ymin=-900,ymax=STATIC_COEFF_INC, color='k', linestyle='--', linewidth=0.5)
    # plt.vlines(x=FRONT_DEADBAND_START_1, ymin=-900, ymax=KINETIC_COEFF_DEC, color='k', linestyle='--', linewidth=0.5)
    # plt.vlines(x=FRONT_DEADBAND_START_2, ymin=-900, ymax=KINETIC_COEFF_INC, color='k', linestyle='--', linewidth=0.5)
    # plt.vlines(x=FRONT_DEADBAND_START_3, ymin=-900, ymax=KINETIC_COEFF_DEC, color='k', linestyle='--', linewidth=0.5)
    # plt.vlines(x=FRONT_DEADBAND_START_4, ymin=-900, ymax=KINETIC_COEFF_INC, color='k', linestyle='--', linewidth=0.5)
    
    # # Plotting Horizontal lines with Input Corresponding to Static and Kinetic Coefficients #
    # plt.axhline(y=STATIC_COEFF_DEC, color='k', linestyle='--', linewidth=0.5)
    # plt.axhline(y=STATIC_COEFF_INC, color='k', linestyle='--', linewidth=0.5)
    # plt.axhline(y=KINETIC_COEFF_DEC, color='k', linestyle='--', linewidth=0.5)
    # plt.axhline(y=KINETIC_COEFF_INC, color='k', linestyle='--', linewidth=0.5)
    
    # # Plotting Individual Points Corresponding to Static and Kinetic Coefficients for Increasing and Reducing Speed #
    # plt.plot(FRONT_DEADBAND_END_1,STATIC_COEFF_DEC,'o', color='tab:orange', label='Static Coefficient for Decreasing Speed', ms=7.5)
    # plt.plot(FRONT_DEADBAND_END_2,STATIC_COEFF_INC,'o', color='tab:pink', label='Static Coefficient for Increasing Speed', ms=7.5)
    # plt.plot(FRONT_DEADBAND_END_3,STATIC_COEFF_DEC,'o', color='tab:orange', ms=7.5)
    # plt.plot(FRONT_DEADBAND_END_4,STATIC_COEFF_INC,'o', color='tab:pink', ms=7.5)
    # plt.plot(FRONT_DEADBAND_START_2,KINETIC_COEFF_INC,'o', color='tab:olive', label='Kinetic Coefficient for Increasing Speed', ms=7.5)
    # plt.plot(FRONT_DEADBAND_START_1,KINETIC_COEFF_DEC,'o', color='tab:cyan', label='Kinetic Coefficient for Decreasing Speed', ms=7.5)
    # plt.plot(FRONT_DEADBAND_START_4,KINETIC_COEFF_INC,'o', color='tab:olive', ms=7.5)
    # plt.plot(FRONT_DEADBAND_START_3,KINETIC_COEFF_DEC,'o', color='tab:cyan', ms=7.5)
    
    # # Adding Axis Labels, y-ticks and sub-plot title #
    # plt.ylabel('Commanded Input (PWM Value)',fontsize=14)
    # plt.xlabel('Time (ms)', fontsize=14)
    # plt.yticks([-800,-600,-400,-170,0,KINETIC_COEFF_DEC,215,400,600,800])
    # plt.ylim([-820,820])
    # plt.legend(loc='upper right', fontsize=14)
    # plt.title('Expected Response', fontsize=14)

    ### Command Response Plot for decreasing speed ###
    plt.subplot(2,2,2)
    NEG_SLOPE_TIME_END = 15209
    plt.scatter(df[df['Relative Time']<= NEG_SLOPE_TIME_END]['Wheel Input'],df[df['Relative Time']<=NEG_SLOPE_TIME_END]['Wheel Speed'])
    
    # Plotting Vertical Lines Corresponding to Static and Kinetic Coefficients #
    plt.axvline(x=STATIC_COEFF_DEC, color='k', linestyle='--',linewidth=0.75)
    plt.axvline(x=KINETIC_COEFF_DEC, color='k', linestyle='--',linewidth=0.75)
    
    # Plotting Horizontal Line to Demarkate Line for No Response Speed #
    plt.axhline(y=0, color='k',linestyle='--',linewidth=0.75)
    
    # Plotting Points at which Static and Kinetic Coefficients are Measured #
    plt.plot(STATIC_COEFF_DEC,0,'o',color='tab:orange',ms=10)
    plt.plot(KINETIC_COEFF_DEC,0,'o',color='tab:cyan', ms=10)
    
    # Setting x-ticks, axese limits, axese labels and sub-plot title #
    plt.xticks([-800,-600,-400,STATIC_COEFF_DEC, 0, KINETIC_COEFF_DEC, 400, 600, 800])
    plt.xlim([400,-400])
    plt.ylim([-30,30])
    plt.ylabel('Response (Degrees Per Second)', fontsize=14)
    plt.title('Deadband Static Coefficient for Reducing Speed', fontsize=14)

    # ### Response vs Time Plot ###
    plt.subplot(2,2,3)
    expected_actual_output(df)
    # plt.plot(df['Relative Time'], df['Wheel Speed'])
    
    # # Plotting Vertical Dotted Lines for Start and End of Deadband #
    # plt.axvline(x=FRONT_DEADBAND_END_1, color='k', linestyle='--', linewidth=0.5)
    # plt.axvline(x=FRONT_DEADBAND_END_2, color='k', linestyle='--', linewidth=0.5)
    # plt.axvline(x=FRONT_DEADBAND_END_3, color='k', linestyle='--', linewidth=0.5)
    # plt.axvline(x=FRONT_DEADBAND_END_4, color='k', linestyle='--', linewidth=0.5)
    # plt.axvline(x=FRONT_DEADBAND_START_1, color='k', linestyle='--', linewidth=0.5)
    # plt.axvline(x=FRONT_DEADBAND_START_2, color='k', linestyle='--', linewidth=0.5)
    # plt.axvline(x=FRONT_DEADBAND_START_3, color='k', linestyle='--', linewidth=0.5)
    # plt.axvline(x=FRONT_DEADBAND_START_4, color='k', linestyle='--', linewidth=0.5)
    
    # # Plotting Colored Dots Corresponding to the Static and Kinetic Coefficients #
    # plt.plot(FRONT_DEADBAND_END_1,0,'o', color='tab:orange', ms=7.5)
    # plt.plot(FRONT_DEADBAND_END_2,0,'o', color='tab:pink', ms=7.5)
    # plt.plot(FRONT_DEADBAND_END_3,0,'o', color='tab:orange', ms=7.5)
    # plt.plot(FRONT_DEADBAND_END_4,0,'o', color='tab:pink', ms=7.5)
    # plt.plot(FRONT_DEADBAND_START_1,0,'o', color='tab:cyan', ms=7.5)
    # plt.plot(FRONT_DEADBAND_START_2,0,'o', color='tab:olive', ms=7.5)
    # plt.plot(FRONT_DEADBAND_START_3,0,'o', color='tab:cyan', ms=7.5)
    # plt.plot(FRONT_DEADBAND_START_4,0,'o', color='tab:olive', ms=7.5)
    
    # # Plotting Axis Labels and Sub-Plot Title #
    # plt.xlabel('Time (ms)',fontsize=14)
    # plt.ylabel('Response (Degrees per Second)',fontsize=14)
    # plt.title('Actual Response', fontsize=14)

    ### Command Response Plot for Increasing Speed #
    plt.subplot(2,2,4)
    POS_SLOPE_TIME_END = 32759
    time = df[df['Relative Time']>=NEG_SLOPE_TIME_END]
    time = time[time['Relative Time']<=POS_SLOPE_TIME_END]
    plt.scatter(time['Wheel Input'],time['Wheel Speed'])
    
    # Plotting Vertical Doted Line for Kinetic and Static Coefficient #
    plt.axvline(x=STATIC_COEFF_INC, color='k', linestyle='--',linewidth=0.75)
    plt.axvline(x=KINETIC_COEFF_INC, color='k', linestyle='--',linewidth=0.75)

    # Plotting Horizonal Dotted Line to Show Where Response is 0 #
    plt.axhline(y=0, color='k',linestyle='--',linewidth=0.75)

    # Plotting Points Demarkating Static and Kinetic Coefficient #
    plt.plot(STATIC_COEFF_INC,0,'o',color='tab:pink', ms=10)
    plt.plot(KINETIC_COEFF_INC,0,'o',color='tab:olive', ms=10)

    # Plotting ticks, setting plot limits and adding axis labels with sub-plot title #
    plt.xticks([-800,-600,-400,KINETIC_COEFF_INC, 0, STATIC_COEFF_INC, 400, 600, 800])
    plt.xlim([-400,400])
    plt.ylim([-30,30])
    plt.xlabel('Commanded Value (PWM Input)', fontsize=14)
    plt.ylabel('Response (Degrees Per Second)', fontsize=14)
    plt.title('Deadband Static Coefficient for Increasing Speed', fontsize=14)

    ### Plotting Final Graph ###
    plt.tight_layout(pad=1.08, w_pad=0.1, h_pad=0.1)
    plt.show()

def real_effective_input(df):
    df['Effective Input'] = df['Wheel Speed Corrected'].apply(effective_input)
    plt.plot(df['Relative Time'], df['Wheel Input'], label = 'Actual Input')
    # plt.plot(df['Relative Time'], df['Effective Input'], label = 'Effective Input')
    
    # Plotting Vertical Lines at Times where deadband is entered and exitted #
    plt.vlines(x=FRONT_DEADBAND_END_1, ymin=-900, ymax=STATIC_COEFF_DEC, color='k', linestyle='--', linewidth=0.5)
    plt.vlines(x=FRONT_DEADBAND_END_2, ymin=-900, ymax=STATIC_COEFF_INC, color='k', linestyle='--', linewidth=0.5)
    plt.vlines(x=FRONT_DEADBAND_END_3, ymin=-900, ymax=STATIC_COEFF_DEC, color='k', linestyle='--', linewidth=0.5)
    plt.vlines(x=FRONT_DEADBAND_END_4, ymin=-900,ymax=STATIC_COEFF_INC, color='k', linestyle='--', linewidth=0.5)
    plt.vlines(x=FRONT_DEADBAND_START_1, ymin=-900, ymax=KINETIC_COEFF_DEC, color='k', linestyle='--', linewidth=0.5)
    plt.vlines(x=FRONT_DEADBAND_START_2, ymin=-900, ymax=KINETIC_COEFF_INC, color='k', linestyle='--', linewidth=0.5)
    plt.vlines(x=FRONT_DEADBAND_START_3, ymin=-900, ymax=KINETIC_COEFF_DEC, color='k', linestyle='--', linewidth=0.5)
    plt.vlines(x=FRONT_DEADBAND_START_4, ymin=-900, ymax=KINETIC_COEFF_INC, color='k', linestyle='--', linewidth=0.5)
    
    # Plotting Horizontal lines with Input Corresponding to Static and Kinetic Coefficients #
    plt.axhline(y=STATIC_COEFF_DEC, color='k', linestyle='--', linewidth=0.5)
    plt.axhline(y=STATIC_COEFF_INC, color='k', linestyle='--', linewidth=0.5)
    plt.axhline(y=KINETIC_COEFF_DEC, color='k', linestyle='--', linewidth=0.5)
    plt.axhline(y=KINETIC_COEFF_INC, color='k', linestyle='--', linewidth=0.5)
    
    # Plotting Individual Points Corresponding to Static and Kinetic Coefficients for Increasing and Reducing Speed #
    plt.plot(FRONT_DEADBAND_END_1,STATIC_COEFF_DEC,'o', color='tab:orange', label='Static Coefficient for Decreasing Speed', ms=7.5)
    plt.plot(FRONT_DEADBAND_END_2,STATIC_COEFF_INC,'o', color='tab:pink', label='Static Coefficient for Increasing Speed', ms=7.5)
    plt.plot(FRONT_DEADBAND_END_3,STATIC_COEFF_DEC,'o', color='tab:orange', ms=7.5)
    plt.plot(FRONT_DEADBAND_END_4,STATIC_COEFF_INC,'o', color='tab:pink', ms=7.5)
    plt.plot(FRONT_DEADBAND_START_2,KINETIC_COEFF_INC,'o', color='tab:olive', label='Kinetic Coefficient for Increasing Speed', ms=7.5)
    plt.plot(FRONT_DEADBAND_START_1,KINETIC_COEFF_DEC,'o', color='tab:cyan', label='Kinetic Coefficient for Decreasing Speed', ms=7.5)
    plt.plot(FRONT_DEADBAND_START_4,KINETIC_COEFF_INC,'o', color='tab:olive', ms=7.5)
    plt.plot(FRONT_DEADBAND_START_3,KINETIC_COEFF_DEC,'o', color='tab:cyan', ms=7.5)
    
    # Adding Axis Labels, y-ticks and sub-plot title #
    plt.ylabel('Commanded Input (PWM Value)',fontsize=14)
    plt.xlabel('Time (ms)', fontsize=14)
    plt.yticks([-800,-600,-400,-170,0,KINETIC_COEFF_DEC,215,400,600,800])
    plt.ylim([-820,820])
    plt.legend(loc='upper right', fontsize=14)
    plt.title('Actual and Effective Input', fontsize=14)

def expected_actual_output(df):
    df['Expected Response'] = df['Wheel Input'].apply(expected_output)
    df['Wheel Speed Corrected'] = df['Wheel Speed']*8
    
    ### Command vs Time Plot ###
    plt.plot(df['Relative Time'], df['Wheel Speed Corrected'], label='Actual Response')
    plt.plot(df['Relative Time'], df['Expected Response'], label='Expected Response', color='gray')

    # Plotting Vertical Dotted Lines for Start and End of Deadband #
    plt.axvline(x=FRONT_DEADBAND_END_1, color='k', linestyle='--', linewidth=0.5)
    plt.axvline(x=FRONT_DEADBAND_END_2, color='k', linestyle='--', linewidth=0.5)
    plt.axvline(x=FRONT_DEADBAND_END_3, color='k', linestyle='--', linewidth=0.5)
    plt.axvline(x=FRONT_DEADBAND_END_4, color='k', linestyle='--', linewidth=0.5)
    plt.axvline(x=FRONT_DEADBAND_START_1, color='k', linestyle='--', linewidth=0.5)
    plt.axvline(x=FRONT_DEADBAND_START_2, color='k', linestyle='--', linewidth=0.5)
    plt.axvline(x=FRONT_DEADBAND_START_3, color='k', linestyle='--', linewidth=0.5)
    plt.axvline(x=FRONT_DEADBAND_START_4, color='k', linestyle='--', linewidth=0.5)
    
    # Plotting Colored Dots Corresponding to the Static and Kinetic Coefficients #
    plt.plot(FRONT_DEADBAND_END_1,0,'o', color='tab:orange', ms=7.5)
    plt.plot(FRONT_DEADBAND_END_2,0,'o', color='tab:pink', ms=7.5)
    plt.plot(FRONT_DEADBAND_END_3,0,'o', color='tab:orange', ms=7.5)
    plt.plot(FRONT_DEADBAND_END_4,0,'o', color='tab:pink', ms=7.5)
    plt.plot(FRONT_DEADBAND_START_1,0,'o', color='tab:cyan', ms=7.5)
    plt.plot(FRONT_DEADBAND_START_2,0,'o', color='tab:olive', ms=7.5)
    plt.plot(FRONT_DEADBAND_START_3,0,'o', color='tab:cyan', ms=7.5)
    plt.plot(FRONT_DEADBAND_START_4,0,'o', color='tab:olive', ms=7.5)
    
    # Plotting Axis Labels and Sub-Plot Title #
    plt.xlabel('Time (ms)',fontsize=14)
    plt.ylabel('Response (Degrees per Second)',fontsize=14)
    plt.legend(fontsize=14)
    plt.title('Expected and Actual Response', fontsize=14)

    # plt.show()

def expected_output(pwm):
    PWM_RESOLUTION = 4095
    MOTOR_RPM = 500
    ratio = pwm/PWM_RESOLUTION
    expected_speed = (MOTOR_RPM/60)* ratio * 360
    return expected_speed

def effective_input(speed):
    PWM_RESOLUTION = 4095
    MOTOR_RPM = 500
    effective_input = (60/MOTOR_RPM)*PWM_RESOLUTION*(1/360)*speed
    return effective_input

if __name__ == '__main__':
    plot_front()
    # plot_rear()
    # plot_front_compensated()
    # plot_rear_compensated()
    # command_response_front()
    # expected_actual()