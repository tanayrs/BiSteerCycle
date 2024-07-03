import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import csv

def sign(num):
    if num > 0:
        return 1
    return -1

def find_constants(path, constants_path, deadbands_path):
    # Readiong in Data into the DataFrame #
    df = pd.read_csv(path)
    df['Relative Time'] = df['Time'] - df['Time'].iloc[0]

    # Calculating Slope Ends where the Wheel Input takes Maximum Value and finding Corresponing Time #
    slope_ends = {'positive':df.iloc[df['Wheel Input'].idxmax()]['Relative Time'],
                'negative':df.iloc[df['Wheel Input'].idxmin()]['Relative Time']}               

    # Empty Lists for Deadband Starts, Ends and Coefficients #
    deadband_starts = []
    deadband_ends = []
    kinetic_coeffs = []
    static_coeffs = []

    # Delay to prevent incorrect measurement of static coefficient #
    if speed < 10:
        static_delay = 2000
    elif speed < 20:
        static_delay = 500
    else:
        static_delay = 0

    # Iterate over Each Measured Instant #
    for i in range(len(df)):
        # Extracting row for current time instant #
        ser = df.iloc[i]

        # If wheel speed is not turning, and was previously turning, potentially a kinetic coefficient #
        if ser['Wheel Speed'] == 0 and df.iloc[i-1]['Wheel Speed'] != 0 and df.iloc[i-2]['Wheel Speed'] != 0  and df.iloc[i-3]['Wheel Speed'] != 0 and df.iloc[i-4]['Wheel Speed'] != 0 :
            # To Prevent Indexing Error with kinetic_coeff #
            if len(kinetic_coeffs) == 0:
                deadband_starts.append(ser['Relative Time'])
                kinetic_coeffs.append(ser['Wheel Input'])
            # If the current instant is suspected to be the kinetic coefficient, it must not have the same sign as the previous kinetic coefficient #
            elif sign(kinetic_coeffs[-1]) != sign(ser['Wheel Input']):
                deadband_starts.append(ser['Relative Time'])
                kinetic_coeffs.append(ser['Wheel Input'])
        
        # If the wheel is about to start turning, and was not turning, potentially a static coefficient #
        if ser['Wheel Speed'] == 0 and df.iloc[i-1]['Wheel Speed'] == 0 and df.iloc[i+1]['Wheel Speed'] != 0 and df.iloc[i+2]['Wheel Speed'] != 0 and  df.iloc[i+3]['Wheel Speed'] != 0 and (ser['Relative Time']-deadband_starts[-1])>static_delay:
            # To Prevent Indexing Error with static_coeffs #
            if len(static_coeffs) == 0:
                deadband_ends.append(ser['Relative Time'])
                static_coeffs.append(ser['Wheel Input'])
            # For the static deadband we want the last point before which the wheel starts continuously turning, until then replace the last suspected point #
            elif sign(static_coeffs[-1]) == sign(ser['Wheel Input']):
                deadband_ends[-1] = ser['Relative Time']
                static_coeffs[-1] = ser['Wheel Input']
            # Append the point to the static coefficients if the sign has changed #
            else:
                deadband_ends.append(ser['Relative Time'])
                static_coeffs.append(ser['Wheel Input'])

    # Finding Kinetic Coefficients in each direction by averaging #
    pos_kinetic = [val for val in kinetic_coeffs if val > 0]
    neg_kinetic = [val for val in kinetic_coeffs if val < 0]
    # kinetic_coeffs = {'increasing':int((sum(neg_kinetic)/len(neg_kinetic))),'decreasing':int(sum(pos_kinetic)/len(pos_kinetic))}

    # Finding Static Coefficients in each direction by averaging #
    pos_static = [val for val in static_coeffs if val > 0]
    neg_static = [val for val in static_coeffs if val < 0]
    # static_coeffs = {'decreasing':int((sum(neg_static)/len(neg_static))),'increasing':int(sum(pos_static)/len(pos_static))}

    # Print all constants#
    # print(f'{deadband_starts=}')
    # print(f'{deadband_ends=}')
    # print(f'{pos_kinetic=}')
    # print(f'{neg_kinetic=}')
    # print(f'{pos_static=}')
    # print(f'{neg_static=}') 

    data_constants = {
        "kinetic_coeffs_dec": pos_kinetic,
        "kinetic_coeffs_inc": neg_kinetic, 
        "static_coeffs_dec": neg_static,
        "static_coeffs_inc": pos_static, 
        }
    
    data_deadbands = {
        "deadband_starts": deadband_starts, 
        "deadband_ends": deadband_ends
    }

    max_len = max(len(v) for v in data_constants.values())
    df_constants = pd.DataFrame({k: [v[i] if i < len(v) else pd.NA for i in range(max_len)] for k, v in data_constants.items()})
    df_constants.to_csv(constants_path,index=False)

    max_len = max(len(v) for v in data_deadbands.values())
    df_deadbands = pd.DataFrame({k: [v[i] if i < len(v) else pd.NA for i in range(max_len)] for k, v in data_deadbands.items()})
    df_deadbands.to_csv(deadbands_path,index=False)

    return slope_ends

def plot_raw_with_measured_constants(path,constants_path,deadbands_path):
    df = pd.read_csv(path)
    df['Relative Time'] = df['Time'] - df['Time'].iloc[0]
    constants_df = pd.read_csv(constants_path)
    deadbands_df = pd.read_csv(deadbands_path)
    # constants_df.dropna(how='any')
    # deadbands_df.dropna(how='any')

    plt.subplot(2,1,1)
    plt.plot(df['Relative Time'],df['Wheel Input'])
    for _,row in deadbands_df.iterrows():
        # print(row['deadband_starts'])
        plt.axvline(x=row['deadband_starts'],color='k',linestyle='--',linewidth=1)
        plt.axvline(x=row['deadband_ends'],color='k',linestyle='--',linewidth=1)
    plt.title(path)
    
    plt.subplot(2,1,2)
    plt.plot(df['Relative Time'],df['Wheel Speed'])
    for _,row in deadbands_df.iterrows():
        # print(row)
        plt.axvline(x=row['deadband_ends'],color='k',linestyle='--',linewidth=1)
        plt.axvline(x=row['deadband_starts'],color='k',linestyle='--',linewidth=1)

    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    plt.show()

if __name__ == '__main__':
    motors = ['Front','Rear']
    speed = 5
    slope_ends_path = "./Python/deadband coeff/SlopeEnds10.csv"
    # with open(slope_ends_path, "w", newline="\n") as f:
    #     csv.writer(f, delimiter=',').writerow(['speed', 'motor', 'positive', 'negative'])

    # path = f'./Python/deadband coeff/SourceData10/{motor}Slope{speed}Data.csv'
    # constants_path = f'./Python/deadband coeff/Constants10/{motor}Slope{speed}Constants.csv'
    # deadbands_path = f'./Python/deadband coeff/Deadbands10/{motor}Slope{speed}Deadbands.csv' 
    # plot_raw_with_measured_constants(path,constants_path,deadbands_path)
    speeds = [2,3,4,7,8,9,10,15,20,30,35,40]

    # speeds = [5,6,1,15,25,30,35,40,20,25,30,35,3]
    # motors = ['Front','Front','Front','Front','Front','Front','Front','Front','Rear','Rear','Rear','Rear','Rear']

    # speeds = [5]
    motors = ['Front','Rear']
    
    for speed in speeds:
    # for speed,motor in zip(speeds,motors):
        for motor in motors:
            path = f'./Python/deadband coeff/SourceData10/{motor}Slope{speed}Data.csv' 
            constants_path = f'./Python/deadband coeff/Constants10/{motor}Slope{speed}Constants.csv'
            deadbands_path = f'./Python/deadband coeff/Deadbands10/{motor}Slope{speed}Deadbands.csv'  

        # plot_raw_with_measured_constants(path,constants_path,deadbands_path)

            slope_ends = find_constants(path, constants_path, deadbands_path)

            with open(slope_ends_path, "a", newline="\n") as f:
                csv.writer(f, delimiter=',').writerow([speed, motor, slope_ends['positive'], slope_ends['negative']])