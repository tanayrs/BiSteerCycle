'''
Experiment: Dead Band Entry Testing
By: Jia Bhargava, Tanay Srinivasa
Last Modified: 24 June 2024

Run bi_steer_cycle_testing arduino code with deadband_test()
'''

from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

# Paths to Files for Front and Rear Deadband Measurements #
FRONT_10_PATH = './Python/dead band slope/SourceData4095/FrontSlope10Data.csv'
REAR_10_PATH = './Python/dead band slope/SourceData4095/RearSlope10Data.csv'
FRONT_20_PATH = './Python/dead band slope/SourceData4095/FrontSlope20Data.csv'
REAR_20_PATH = './Python/dead band slope/SourceData4095/RearSlope20Data.csv'
FRONT_40_PATH = './Python/dead band slope/SourceData4095/FrontSlope40Data_1.csv'
REAR_40_PATH = './Python/dead band slope/SourceData4095/RearSlope40Data.csv'

# Time at Which Front Motor Enters Deadband at Slope 10 per 100ms #
FRONT_10_DEADBAND_START_1 = 5049
FRONT_10_DEADBAND_START_2 = 22484
FRONT_10_DEADBAND_START_3 = 40155
FRONT_10_DEADBAND_START_4 = 57766

# Input Value Corresponding to Deadband #
FRONT_10_DEADBAND_INPUT_START = -135
FRONT_10_DEADBAND_INPUT_END = 130

# Time at Which Rear Motor Enters Deadband at Slope 10 per 100ms #
REAR_10_DEADBAND_START_1 = 7341
REAR_10_DEADBAND_START_2 = 24766
REAR_10_DEADBAND_START_3 = 42319
REAR_10_DEADBAND_START_4 = 59875

# Input Value Corresponding to Deadband #
REAR_10_DEADBAND_INPUT_START = -120
REAR_10_DEADBAND_INPUT_END = 115

# Time at Which Front Motor Enters Deadband at Slope 20 per 100ms #
FRONT_20_DEADBAND_START_1 = 3668
FRONT_20_DEADBAND_START_2 = 12502
FRONT_20_DEADBAND_START_3 = 21278
FRONT_20_DEADBAND_START_4 = 30115

# Input Value Corresponding to Deadband #
FRONT_20_DEADBAND_INPUT_START = -110
FRONT_20_DEADBAND_INPUT_END = 120

# Time at Which Rear Motor Enters Deadband at Slope 20 per 100ms #
REAR_20_DEADBAND_START_1 = 3846
REAR_20_DEADBAND_START_2 = 12743
REAR_20_DEADBAND_START_3 = 21642
REAR_20_DEADBAND_START_4 = 30476

# Input Value Corresponding to Deadband #
REAR_20_DEADBAND_INPUT_START = -100
REAR_20_DEADBAND_INPUT_END = 100

# For FrontSlope40Data.csv #
# Time at Which Front Motor Enters Deadband at Slope 40 per 100ms #
FRONT_40_DEADBAND_START_1 = 1983
FRONT_40_DEADBAND_START_2 = 6312
FRONT_40_DEADBAND_START_3 = 10880
FRONT_40_DEADBAND_START_4 = 15268

# Input Value Corresponding to Deadband #
FRONT_40_DEADBAND_INPUT_START = -90
FRONT_40_DEADBAND_INPUT_END = 70

# For FrontSlope40Data_1.csv #
# Time at Which Front Motor Enters Deadband at Slope 40 per 100ms #
# FRONT_40_DEADBAND_START_1 = 2045
# FRONT_40_DEADBAND_START_2 = 6432
# FRONT_40_DEADBAND_START_3 = 10941
# FRONT_40_DEADBAND_START_4 = 15328

# Input Value Corresponding to Deadband #
# FRONT_40_DEADBAND_INPUT_START = -90
# FRONT_40_DEADBAND_INPUT_END = 70

# Time at Which Rear Motor Enters Deadband at Slope 40 per 100ms #
REAR_40_DEADBAND_START_1 = 1924
REAR_40_DEADBAND_START_2 = 6552
REAR_40_DEADBAND_START_3 = 11065
REAR_40_DEADBAND_START_4 = 15685

# Input Value Corresponding to Deadband #
REAR_40_DEADBAND_INPUT_START = -80
REAR_40_DEADBAND_INPUT_END = 90

def plot_front10():
    # Reading CSV into pandas DataFrame #
    df = pd.read_csv(FRONT_10_PATH)

    # Creating Column with Time Relative to First Entry #
    df['Relative Time'] = df['Time']-df['Time'].iloc[0]
    print(df['Time'].iloc[0])

    # Creating Subplots and Setting Figure Dimensions #
    fig, axs = plt.subplots(2, 1)
    fig.set_figheight(8.5)
    fig.set_figwidth(14)

    # Plotting Input vs Time #
    axs[0].plot(df['Relative Time'], df['Wheel Input'])
    
    # Plotting Vertical Dashed Lines Corresponding to Deadband Start #
    axs[0].axvline(x=FRONT_10_DEADBAND_START_1, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=FRONT_10_DEADBAND_START_2, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=FRONT_10_DEADBAND_START_3, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=FRONT_10_DEADBAND_START_4, color='k', linestyle='--', linewidth=0.5)
    
    # Plotting Horizontal Dashed Lines Corresponding to Deadband Start #
    axs[0].axhline(y=FRONT_10_DEADBAND_INPUT_START, color='k', linestyle='--', linewidth=0.5)
    axs[0].axhline(y=FRONT_10_DEADBAND_INPUT_END, color='k', linestyle='--', linewidth=0.5)
    
    # Plotting Dots Corresponding to Deadband Start #
    axs[0].plot(FRONT_10_DEADBAND_START_1,FRONT_10_DEADBAND_INPUT_END,'o')
    axs[0].plot(FRONT_10_DEADBAND_START_2,FRONT_10_DEADBAND_INPUT_START,'o')
    axs[0].plot(FRONT_10_DEADBAND_START_3,FRONT_10_DEADBAND_INPUT_END,'o')
    axs[0].plot(FRONT_10_DEADBAND_START_4,FRONT_10_DEADBAND_INPUT_START,'o')
    
    # Plot Formatting #
    axs[0].set_ylabel('Commanded Input (PWM Value)',fontsize=14)
    axs[0].set_yticks([-800,-600,-400,-200,-135,0,130,200,400,600,800])
    axs[0].set_xticks([])

    # Plotting Response vs Time #
    axs[1].plot(df['Relative Time'], df['Wheel Speed'])

    # Plotting Vertical Dashed Lines Corresponding to Deadband Start #
    axs[1].axvline(x=FRONT_10_DEADBAND_START_1, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=FRONT_10_DEADBAND_START_2, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=FRONT_10_DEADBAND_START_3, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=FRONT_10_DEADBAND_START_4, color='k', linestyle='--', linewidth=0.5)
    
    # Plotting Dots Corresponding to Deadband Start #
    axs[1].plot(FRONT_10_DEADBAND_START_1,0,'o')
    axs[1].plot(FRONT_10_DEADBAND_START_2,0,'o')
    axs[1].plot(FRONT_10_DEADBAND_START_3,0,'o')
    axs[1].plot(FRONT_10_DEADBAND_START_4,0,'o')

    # Plot Formatting #
    axs[1].set_xlabel('Time (ms)',fontsize=14)
    axs[1].set_ylabel('Response (Degrees per Second)',fontsize=14)

    # Show the plot
    plt.tight_layout()
    plt.show()

    # Plotting Command vs Response #
    sorted_df = df.sort_values('Wheel Input')
    plt.scatter(sorted_df['Wheel Input'],sorted_df['Wheel Speed'])
    plt.xlabel('Commanded Value (PWM Input)', fontsize=14)
    plt.ylabel('Response (Degrees Per Second)', fontsize=14)
    plt.title('Commanded Value vs Response')
    plt.show()

def plot_rear10():
    # Reading CSV into pandas DataFrame #
    df = pd.read_csv(REAR_10_PATH)

    # Creating Column with Time Relative to First Entry #
    df['Relative Time'] = df['Time']-df['Time'].iloc[0]
    print(df['Time'].iloc[0])

    # Creating Subplots and Setting Figure Dimensions #
    fig, axs = plt.subplots(2, 1)
    fig.set_figheight(8.5)
    fig.set_figwidth(14)

    # Plotting Input vs Time #
    axs[0].plot(df['Relative Time'], df['Wheel Input'])

    # Plotting Vertical Dashed Lines Corresponding to Deadband Start #
    axs[0].axvline(x=REAR_10_DEADBAND_START_1, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=REAR_10_DEADBAND_START_2, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=REAR_10_DEADBAND_START_3, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=REAR_10_DEADBAND_START_4, color='k', linestyle='--', linewidth=0.5)

    # Plotting Horizontal Dashed Lines Corresponding to Deadband Start #
    axs[0].axhline(y=REAR_10_DEADBAND_INPUT_START, color='k', linestyle='--', linewidth=0.5)
    axs[0].axhline(y=REAR_10_DEADBAND_INPUT_END, color='k', linestyle='--', linewidth=0.5)

    # Plotting Dots Corresponding to Deadband Start #
    axs[0].plot(REAR_10_DEADBAND_START_1,REAR_10_DEADBAND_INPUT_END,'o')
    axs[0].plot(REAR_10_DEADBAND_START_2,REAR_10_DEADBAND_INPUT_START,'o')
    axs[0].plot(REAR_10_DEADBAND_START_3,REAR_10_DEADBAND_INPUT_END,'o')
    axs[0].plot(REAR_10_DEADBAND_START_4,REAR_10_DEADBAND_INPUT_START,'o')

    # Plot Formatting #
    axs[0].set_ylabel('Commanded Input (PWM Value)',fontsize=14)
    axs[0].set_yticks([-800,-600,-400,-200,-120,0,115,200,400,600,800])
    axs[0].set_xticks([])

    # Plotting Response vs Time #
    axs[1].plot(df['Relative Time'], df['Wheel Speed'])

    # Plotting Vertical Dashed Lines Corresponding to Deadband Start #
    axs[1].axvline(x=REAR_10_DEADBAND_START_1, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=REAR_10_DEADBAND_START_2, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=REAR_10_DEADBAND_START_3, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=REAR_10_DEADBAND_START_4, color='k', linestyle='--', linewidth=0.5)

    # Plotting Dots Corresponding to Deadband Start #
    axs[1].plot(REAR_10_DEADBAND_START_1,0,'o')
    axs[1].plot(REAR_10_DEADBAND_START_2,0,'o')
    axs[1].plot(REAR_10_DEADBAND_START_3,0,'o')
    axs[1].plot(REAR_10_DEADBAND_START_4,0,'o')

    # Plot Formatting #
    axs[1].set_xlabel('Time (ms)',fontsize=14)
    axs[1].set_ylabel('Response (Degrees per Second)',fontsize=14)

    # Show the plot
    plt.tight_layout()
    plt.show()

    # Plotting Command vs Response #
    sorted_df = df.sort_values('Wheel Input')
    plt.scatter(sorted_df['Wheel Input'],sorted_df['Wheel Speed'])
    plt.xlabel('Commanded Value (PWM Input)')
    plt.ylabel('Response (Degrees Per Second)')
    plt.title('Commanded Value vs Response')
    plt.show()

def plot_front20():
    # Reading CSV into pandas DataFrame #
    df = pd.read_csv(FRONT_20_PATH)

    # Creating Column with Time Relative to First Entry #
    df['Relative Time'] = df['Time']-df['Time'].iloc[0]
    print(df['Time'].iloc[0])

    # Creating Subplots and Setting Figure Dimensions #
    fig, axs = plt.subplots(2, 1)
    fig.set_figheight(8.5)
    fig.set_figwidth(14)

    # Plotting Input vs Time #
    axs[0].plot(df['Relative Time'], df['Wheel Input'])

    # Plotting Vertical Dashed Lines Corresponding to Deadband Start #
    axs[0].axvline(x=FRONT_20_DEADBAND_START_1, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=FRONT_20_DEADBAND_START_2, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=FRONT_20_DEADBAND_START_3, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=FRONT_20_DEADBAND_START_4, color='k', linestyle='--', linewidth=0.5)
    
    axs[0].axhline(y=FRONT_20_DEADBAND_INPUT_START, color='k', linestyle='--', linewidth=0.5)
    axs[0].axhline(y=FRONT_20_DEADBAND_INPUT_END, color='k', linestyle='--', linewidth=0.5)
    
    axs[0].plot(FRONT_20_DEADBAND_START_1,FRONT_20_DEADBAND_INPUT_END,'o')
    axs[0].plot(FRONT_20_DEADBAND_START_2,FRONT_20_DEADBAND_INPUT_START,'o')
    axs[0].plot(FRONT_20_DEADBAND_START_3,FRONT_20_DEADBAND_INPUT_END,'o')
    axs[0].plot(FRONT_20_DEADBAND_START_4,FRONT_20_DEADBAND_INPUT_START,'o')
    
    axs[0].set_ylabel('Commanded Input (PWM Value)',fontsize=14)
    axs[0].set_yticks([-800,-600,-400,-200,-110,0,120,200,400,600,800])
    axs[0].set_xticks([])
    # axs[0].set_title('Commanded Input vs Time')

    # Plot on the second axis
    axs[1].plot(df['Relative Time'], df['Wheel Speed'])
    axs[1].axvline(x=FRONT_20_DEADBAND_START_1, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=FRONT_20_DEADBAND_START_2, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=FRONT_20_DEADBAND_START_3, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=FRONT_20_DEADBAND_START_4, color='k', linestyle='--', linewidth=0.5)
    
    axs[1].plot(FRONT_20_DEADBAND_START_1,0,'o')
    axs[1].plot(FRONT_20_DEADBAND_START_2,0,'o')
    axs[1].plot(FRONT_20_DEADBAND_START_3,0,'o')
    axs[1].plot(FRONT_20_DEADBAND_START_4,0,'o')
    
    axs[1].set_xlabel('Time (ms)',fontsize=14)
    axs[1].set_ylabel('Response (Degrees per Second)',fontsize=14)

    # Show the plot
    plt.tight_layout()
    plt.show()

    sorted_df = df.sort_values('Wheel Input')
    plt.scatter(sorted_df['Wheel Input'],sorted_df['Wheel Speed'])
    plt.xlabel('Commanded Value (PWM Input)')
    plt.ylabel('Response (Degrees Per Second)')
    plt.title('Commanded Value vs Response')
    plt.show()

def plot_rear20():
    # Reading CSV into pandas DataFrame #
    df = pd.read_csv(REAR_20_PATH)
    df['Relative Time'] = df['Time']-df['Time'].iloc[0]
    print(df['Time'].iloc[0])

    # Plotting Angle vs Time #
    fig, axs = plt.subplots(2, 1)
    fig.set_figheight(8.5)
    fig.set_figwidth(14)

    # Plot on the first axis
    axs[0].plot(df['Relative Time'], df['Wheel Input'])
    
    axs[0].axvline(x=REAR_20_DEADBAND_START_1, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=REAR_20_DEADBAND_START_2, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=REAR_20_DEADBAND_START_3, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=REAR_20_DEADBAND_START_4, color='k', linestyle='--', linewidth=0.5)
    
    axs[0].axhline(y=REAR_20_DEADBAND_INPUT_START, color='k', linestyle='--', linewidth=0.5)
    axs[0].axhline(y=REAR_20_DEADBAND_INPUT_END, color='k', linestyle='--', linewidth=0.5)
    
    axs[0].plot(REAR_20_DEADBAND_START_1,REAR_20_DEADBAND_INPUT_END,'o')
    axs[0].plot(REAR_20_DEADBAND_START_2,REAR_20_DEADBAND_INPUT_START,'o')
    axs[0].plot(REAR_20_DEADBAND_START_3,REAR_20_DEADBAND_INPUT_END,'o')
    axs[0].plot(REAR_20_DEADBAND_START_4,REAR_20_DEADBAND_INPUT_START,'o')
    
    axs[0].set_ylabel('Commanded Input (PWM Value)',fontsize=14)
    axs[0].set_yticks([-800,-600,-400,-200,-100,0,100,200,400,600,800])
    axs[0].set_xticks([])

    # Plot on the second axis
    axs[1].plot(df['Relative Time'], df['Wheel Speed'])
    axs[1].axvline(x=REAR_20_DEADBAND_START_1, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=REAR_20_DEADBAND_START_2, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=REAR_20_DEADBAND_START_3, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=REAR_20_DEADBAND_START_4, color='k', linestyle='--', linewidth=0.5)
    
    axs[1].plot(REAR_20_DEADBAND_START_1,0,'o')
    axs[1].plot(REAR_20_DEADBAND_START_2,0,'o')
    axs[1].plot(REAR_20_DEADBAND_START_3,0,'o')
    axs[1].plot(REAR_20_DEADBAND_START_4,0,'o')
    axs[1].set_xlabel('Time (ms)',fontsize=14)
    axs[1].set_ylabel('Response (Degrees per Second)',fontsize=14)

    # Show the plot
    plt.tight_layout()
    plt.show()

    sorted_df = df.sort_values('Wheel Input')
    plt.scatter(sorted_df['Wheel Input'],sorted_df['Wheel Speed'])
    plt.xlabel('Commanded Value (PWM Input)')
    plt.ylabel('Response (Degrees Per Second)')
    plt.title('Commanded Value vs Response')
    plt.show()

def plot_front40():
    # Reading CSV into pandas DataFrame #
    df = pd.read_csv(FRONT_40_PATH)
    df['Relative Time'] = df['Time']-df['Time'].iloc[0]
    print(df['Time'].iloc[0])

    # Plotting Angle vs Time #
    fig, axs = plt.subplots(2, 1)
    fig.set_figheight(8.5)
    fig.set_figwidth(14)

    # Plot on the first axis
    axs[0].plot(df['Relative Time'], df['Wheel Input'])
    axs[0].axvline(x=FRONT_40_DEADBAND_START_1, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=FRONT_40_DEADBAND_START_2, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=FRONT_40_DEADBAND_START_3, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=FRONT_40_DEADBAND_START_4, color='k', linestyle='--', linewidth=0.5)
    
    axs[0].axhline(y=FRONT_40_DEADBAND_INPUT_START, color='k', linestyle='--', linewidth=0.5)
    axs[0].axhline(y=FRONT_40_DEADBAND_INPUT_END, color='k', linestyle='--', linewidth=0.5)
    
    axs[0].plot(FRONT_40_DEADBAND_START_1,FRONT_40_DEADBAND_INPUT_END,'o')
    axs[0].plot(FRONT_40_DEADBAND_START_2,FRONT_40_DEADBAND_INPUT_START,'o')
    axs[0].plot(FRONT_40_DEADBAND_START_3,FRONT_40_DEADBAND_INPUT_END,'o')
    axs[0].plot(FRONT_40_DEADBAND_START_4,FRONT_40_DEADBAND_INPUT_START,'o')
    
    axs[0].set_ylabel('Commanded Input (PWM Value)',fontsize=14)
    axs[0].set_yticks([-800,-600,-400,-200,-90,0,70,200,400,600,800])
    axs[0].set_xticks([])
    # axs[0].set_title('Commanded Input vs Time')

    # Plot on the second axis
    axs[1].plot(df['Relative Time'], df['Wheel Speed'])
    axs[1].axvline(x=FRONT_40_DEADBAND_START_1, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=FRONT_40_DEADBAND_START_2, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=FRONT_40_DEADBAND_START_3, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=FRONT_40_DEADBAND_START_4, color='k', linestyle='--', linewidth=0.5)
    
    axs[1].plot(FRONT_40_DEADBAND_START_1,0,'o')
    axs[1].plot(FRONT_40_DEADBAND_START_2,0,'o')
    axs[1].plot(FRONT_40_DEADBAND_START_3,0,'o')
    axs[1].plot(FRONT_40_DEADBAND_START_4,0,'o')
    
    axs[1].set_xlabel('Time (ms)',fontsize=14)
    axs[1].set_ylabel('Response (Degrees per Second)',fontsize=14)

    # Show the plot
    plt.tight_layout()
    plt.show()

    sorted_df = df.sort_values('Wheel Input')
    plt.scatter(sorted_df['Wheel Input'],sorted_df['Wheel Speed'])
    plt.xlabel('Commanded Value (PWM Input)')
    plt.ylabel('Response (Degrees Per Second)')
    plt.title('Commanded Value vs Response')
    plt.show()

def plot_rear40():
    # Reading CSV into pandas DataFrame #
    df = pd.read_csv(REAR_40_PATH)
    df['Relative Time'] = df['Time']-df['Time'].iloc[0]
    print(df['Time'].iloc[0])

    # Plotting Angle vs Time #
    fig, axs = plt.subplots(2, 1)
    fig.set_figheight(8.5)
    fig.set_figwidth(14)

    # Plot on the first axis
    axs[0].plot(df['Relative Time'], df['Wheel Input'])
    
    axs[0].axvline(x=REAR_40_DEADBAND_START_1, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=REAR_40_DEADBAND_START_2, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=REAR_40_DEADBAND_START_3, color='k', linestyle='--', linewidth=0.5)
    axs[0].axvline(x=REAR_40_DEADBAND_START_4, color='k', linestyle='--', linewidth=0.5)
    
    axs[0].axhline(y=REAR_40_DEADBAND_INPUT_START, color='k', linestyle='--', linewidth=0.5)
    axs[0].axhline(y=REAR_40_DEADBAND_INPUT_END, color='k', linestyle='--', linewidth=0.5)
    
    axs[0].plot(REAR_40_DEADBAND_START_1,REAR_40_DEADBAND_INPUT_END,'o')
    axs[0].plot(REAR_40_DEADBAND_START_2,REAR_40_DEADBAND_INPUT_START,'o')
    axs[0].plot(REAR_40_DEADBAND_START_3,REAR_40_DEADBAND_INPUT_END,'o')
    axs[0].plot(REAR_40_DEADBAND_START_4,REAR_40_DEADBAND_INPUT_START,'o')
    
    axs[0].set_ylabel('Commanded Input (PWM Value)',fontsize=14)
    axs[0].set_yticks([-800,-600,-400,-200,-80,0,90,200,400,600,800])
    axs[0].set_xticks([])

    # Plot on the second axis
    axs[1].plot(df['Relative Time'], df['Wheel Speed'])
    axs[1].axvline(x=REAR_40_DEADBAND_START_1, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=REAR_40_DEADBAND_START_2, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=REAR_40_DEADBAND_START_3, color='k', linestyle='--', linewidth=0.5)
    axs[1].axvline(x=REAR_40_DEADBAND_START_4, color='k', linestyle='--', linewidth=0.5)
    
    axs[1].plot(REAR_40_DEADBAND_START_1,0,'o')
    axs[1].plot(REAR_40_DEADBAND_START_2,0,'o')
    axs[1].plot(REAR_40_DEADBAND_START_3,0,'o')
    axs[1].plot(REAR_40_DEADBAND_START_4,0,'o')
    axs[1].set_xlabel('Time (ms)',fontsize=14)
    axs[1].set_ylabel('Response (Degrees per Second)',fontsize=14)

    # Show the plot
    plt.tight_layout()
    plt.show()

    sorted_df = df.sort_values('Wheel Input')
    plt.scatter(sorted_df['Wheel Input'],sorted_df['Wheel Speed'])
    plt.xlabel('Commanded Value (PWM Input)')
    plt.ylabel('Response (Degrees Per Second)')
    plt.title('Commanded Value vs Response')
    plt.show()

if __name__ == '__main__':
    # plot_front10()
    # plot_rear10()
    # plot_front20()
    # plot_rear20()
    plot_front40()
    # plot_rear40()
