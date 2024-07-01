'''
Experiment: Finding Kinetic and Static Friction Coefficients
By: Jia Bhargava, Tanay Srinivasa
Last Modified: 1 Jul 2024

Run bi_steer_cycle_testing arduino code with deadband_test()
'''

from matplotlib import pyplot as plt
import pandas as pd

PLOTTING_CONSTANTS_PATH = './Python/deadband coeff/plotting_constants.csv'

class MotorCompensation:
    def __init__(self, file_path, deadband_starts, deadband_ends, kinetic_coeffs, static_coeffs, slope_ends):
        self.df = pd.read_csv(file_path)
        self.df['Relative Time'] = self.df['Time']-self.df['Time'].iloc[0]
        
        self.deadband_starts = deadband_starts
        self.deadband_ends = deadband_ends
        self.kinetic_coeffs = kinetic_coeffs
        self.static_coeffs = static_coeffs
        self.slope_ends = slope_ends

    def plot_compensation(self):
        plt.figure(figsize=(14,8.5))
        
        ### Command vs Time Plot ###
        plt.subplot(2,2,1)
        self.__plot_input()

        ### Command Response Plot for decreasing speed ###
        plt.subplot(2,2,2)
        self.__plot_cr_decreasing()

        # ### Response vs Time Plot ###
        plt.subplot(2,2,3)
        self.__plot_output()

        ### Command Response Plot for Increasing Speed #
        plt.subplot(2,2,4)
        self.__plot_cr_increasing()

        ### Plotting Final Graph ###
        plt.tight_layout(pad=1.08, w_pad=0.1, h_pad=0.1)
        plt.show()

    def __plot_input(self):
        self.df['Effective Input'] = self.df['Wheel Speed'].apply(self.__calculate_effective_input)
        plt.plot(self.df['Relative Time'], self.df['Wheel Input'])
        # plt.plot(self.df['Relative Time'], self.df['Wheel Input'], label = 'Actual Input')
        # plt.plot(self.df['Relative Time'], self.df['Effective Input'], label = 'Effective Input')
        
        # Plotting Vertical Lines at Times where deadband is entered and exitted #
        plt.vlines(x=self.deadband_ends[0], ymin=-900, ymax=self.static_coeffs['decreasing'], color='k', linestyle='--', linewidth=0.5)
        plt.vlines(x=self.deadband_ends[1], ymin=-900, ymax=self.static_coeffs['increasing'], linestyle='--', linewidth=0.5)
        plt.vlines(x=self.deadband_ends[2], ymin=-900, ymax=self.static_coeffs['decreasing'], color='k', linestyle='--', linewidth=0.5)
        plt.vlines(x=self.deadband_ends[3], ymin=-900,ymax=self.static_coeffs['increasing'], color='k', linestyle='--', linewidth=0.5)
        plt.vlines(x=self.deadband_starts[0], ymin=-900, ymax=self.kinetic_coeffs['decreasing'], color='k', linestyle='--', linewidth=0.5)
        plt.vlines(x=self.deadband_starts[1], ymin=-900, ymax=self.kinetic_coeffs['increasing'], color='k', linestyle='--', linewidth=0.5)
        plt.vlines(x=self.deadband_starts[2], ymin=-900, ymax=self.kinetic_coeffs['decreasing'], color='k', linestyle='--', linewidth=0.5)
        plt.vlines(x=self.deadband_starts[3], ymin=-900, ymax=self.kinetic_coeffs['increasing'], color='k', linestyle='--', linewidth=0.5)
        
        # Plotting Horizontal lines with Input Corresponding to Static and Kinetic Coefficients #
        plt.axhline(y=self.static_coeffs['decreasing'], color='k', linestyle='--', linewidth=0.5)
        plt.axhline(y=self.static_coeffs['increasing'], color='k', linestyle='--', linewidth=0.5)
        plt.axhline(y=self.kinetic_coeffs['decreasing'], color='k', linestyle='--', linewidth=0.5)
        plt.axhline(y=self.kinetic_coeffs['increasing'], color='k', linestyle='--', linewidth=0.5)
        
        # Plotting Individual Points Corresponding to Static and Kinetic Coefficients for Increasing and Reducing Speed #
        plt.plot(self.deadband_ends[0],self.static_coeffs['decreasing'],'o', color='tab:orange', label='Static Coefficient for Decreasing Speed', ms=7.5)
        plt.plot(self.deadband_ends[1],self.static_coeffs['increasing'],'o', color='tab:pink', label='Static Coefficient for Increasing Speed', ms=7.5)
        plt.plot(self.deadband_ends[2],self.static_coeffs['decreasing'],'o', color='tab:orange', ms=7.5)
        plt.plot(self.deadband_ends[3],self.static_coeffs['increasing'],'o', color='tab:pink', ms=7.5)

        plt.plot(self.deadband_starts[0],self.kinetic_coeffs['decreasing'],'o', color='tab:cyan', label='Kinetic Coefficient for Decreasing Speed', ms=7.5)
        plt.plot(self.deadband_starts[1],self.kinetic_coeffs['increasing'],'o', color='tab:olive', label='Kinetic Coefficient for Increasing Speed', ms=7.5)
        plt.plot(self.deadband_starts[2],self.kinetic_coeffs['decreasing'],'o', color='tab:cyan', ms=7.5)
        plt.plot(self.deadband_starts[3],self.kinetic_coeffs['increasing'],'o', color='tab:olive', ms=7.5)
        
        # Adding Axis Labels, y-ticks and sub-plot title #
        plt.ylabel('Commanded Input (PWM Value)',fontsize=14)
        plt.xlabel('Time (ms)', fontsize=14)
        plt.yticks([-800,-600,-400,self.static_coeffs['decreasing'],0,self.kinetic_coeffs['decreasing'],self.static_coeffs['increasing'],400,600,800])
        plt.ylim([-820,820])
        plt.legend(loc='upper right', fontsize=14)
        plt.title('Input', fontsize=14)

    def __plot_output(self):
        self.df['Expected Response'] = self.df['Wheel Input'].apply(self.__calculate_expected_output)
        
        ### Command vs Time Plot ###
        plt.plot(self.df['Relative Time'], self.df['Wheel Speed'], label='Actual Response')
        plt.plot(self.df['Relative Time'], self.df['Expected Response'], label='Expected Response', color='gray')

        # Plotting Vertical Dotted Lines for Start and End of Deadband #
        plt.axvline(x=self.deadband_ends[0], color='k', linestyle='--', linewidth=0.5)
        plt.axvline(x=self.deadband_ends[1], color='k', linestyle='--', linewidth=0.5)
        plt.axvline(x=self.deadband_ends[2], color='k', linestyle='--', linewidth=0.5)
        plt.axvline(x=self.deadband_ends[3], color='k', linestyle='--', linewidth=0.5)
        plt.axvline(x=self.deadband_starts[0], color='k', linestyle='--', linewidth=0.5)
        plt.axvline(x=self.deadband_starts[1], color='k', linestyle='--', linewidth=0.5)
        plt.axvline(x=self.deadband_starts[2], color='k', linestyle='--', linewidth=0.5)
        plt.axvline(x=self.deadband_starts[3], color='k', linestyle='--', linewidth=0.5)
        
        # Plotting Colored Dots Corresponding to the Static and Kinetic Coefficients #
        plt.plot(self.deadband_ends[0],0,'o', color='tab:orange', ms=7.5)
        plt.plot(self.deadband_ends[1],0,'o', color='tab:pink', ms=7.5)
        plt.plot(self.deadband_ends[2],0,'o', color='tab:orange', ms=7.5)
        plt.plot(self.deadband_ends[3],0,'o', color='tab:pink', ms=7.5)
        plt.plot(self.deadband_starts[0],0,'o', color='tab:cyan', ms=7.5)
        plt.plot(self.deadband_starts[1],0,'o', color='tab:olive', ms=7.5)
        plt.plot(self.deadband_starts[2],0,'o', color='tab:cyan', ms=7.5)
        plt.plot(self.deadband_starts[3],0,'o', color='tab:olive', ms=7.5)
        
        # Plotting Axis Labels and Sub-Plot Title #
        plt.xlabel('Time (ms)',fontsize=14)
        plt.ylabel('Response (Degrees per Second)',fontsize=14)
        plt.legend(fontsize=14)
        plt.title('Expected and Actual Response', fontsize=14)

        # plt.show()

    def __plot_cr_decreasing(self):
        plt.scatter(
            self.df[self.df['Relative Time']<= self.slope_ends['negative']]['Wheel Input'],
            self.df[self.df['Relative Time']<=self.slope_ends['negative']]['Wheel Speed']
            )
        
        # Plotting Vertical Lines Corresponding to Static and Kinetic Coefficients #
        plt.axvline(x=self.static_coeffs['decreasing'], color='k', linestyle='--',linewidth=0.75)
        plt.axvline(x=self.kinetic_coeffs['decreasing'], color='k', linestyle='--',linewidth=0.75)
        
        # Plotting Horizontal Line to Demarkate Line for No Response Speed #
        plt.axhline(y=0, color='k',linestyle='--',linewidth=0.75)
        
        # Plotting Points at which Static and Kinetic Coefficients are Measured #
        plt.plot(self.static_coeffs['decreasing'],0,'o',color='tab:orange',ms=10)
        plt.plot(self.kinetic_coeffs['decreasing'],0,'o',color='tab:cyan', ms=10)
        
        # Setting x-ticks, axese limits, axese labels and sub-plot title #
        plt.xticks([-800,-600,-400,self.static_coeffs['decreasing'], 0, self.kinetic_coeffs['decreasing'], 400, 600, 800])
        plt.xlim([400,-400])
        plt.ylim([-self.df['Wheel Speed'].max()/3,self.df['Wheel Speed'].max()/3])
        plt.ylabel('Response (Degrees Per Second)', fontsize=14)
        plt.title('Deadband Static Coefficient for Reducing Speed', fontsize=14)

    def __plot_cr_increasing(self):
        time = self.df[self.df['Relative Time']>=self.slope_ends['negative']]
        time = time[time['Relative Time']<=self.slope_ends['positive']]
        plt.scatter(time['Wheel Input'],time['Wheel Speed'])
        
        # Plotting Vertical Doted Line for Kinetic and Static Coefficient #
        plt.axvline(x=self.static_coeffs['increasing'], color='k', linestyle='--',linewidth=0.75)
        plt.axvline(x=self.kinetic_coeffs['increasing'], color='k', linestyle='--',linewidth=0.75)

        # Plotting Horizonal Dotted Line to Show Where Response is 0 #
        plt.axhline(y=0, color='k',linestyle='--',linewidth=0.75)

        # Plotting Points Demarkating Static and Kinetic Coefficient #
        plt.plot(self.static_coeffs['increasing'],0,'o',color='tab:pink', ms=10)
        plt.plot(self.kinetic_coeffs['increasing'],0,'o',color='tab:olive', ms=10)

        # Plotting ticks, setting plot limits and adding axis labels with sub-plot title #
        plt.xticks([-800,-600,-400,self.kinetic_coeffs['increasing'], 0, self.static_coeffs['increasing'], 400, 600, 800])
        plt.xlim([-400,400])
        plt.ylim([-self.df['Wheel Speed'].max()/3,self.df['Wheel Speed'].max()/3])
        plt.xlabel('Commanded Value (PWM Input)', fontsize=14)
        plt.ylabel('Response (Degrees Per Second)', fontsize=14)
        plt.title('Deadband Static Coefficient for Increasing Speed', fontsize=14)

    def __calculate_expected_output(self,pwm):
        PWM_RESOLUTION = 4095
        MOTOR_RPM = 500
        ratio = pwm/PWM_RESOLUTION
        expected_speed = (MOTOR_RPM/60)* ratio * 360
        return expected_speed

    def __calculate_effective_input(self,speed):
        PWM_RESOLUTION = 4095
        MOTOR_RPM = 500
        effective_input = (60/MOTOR_RPM)*PWM_RESOLUTION*(1/360)*speed
        return effective_input

def plot_motor_data(speed,motor):
    df = pd.read_csv(PLOTTING_CONSTANTS_PATH)
    ser = df.loc[(df['speed']==speed) & (df['motor']==motor)]
    file_path = ser['path'].values[0]
    deadband_starts = [ser['deadband_start1'].values[0], ser['deadband_start2'].values[0], ser['deadband_start3'].values[0], ser['deadband_start4'].values[0]]
    deadband_ends = [ser['deadband_end1'].values[0], ser['deadband_end2'].values[0], ser['deadband_end3'].values[0], ser['deadband_end4'].values[0]]
    kinetic_coeffs = {'increasing':ser['kinetic_coeff_inc'].values[0],'decreasing':ser['kinetic_coeff_dec'].values[0]}
    static_coeffs = {'increasing': ser['static_coeff_inc'].values[0], 'decreasing':ser['static_coeff_dec'].values[0]}
    slope_ends = {'positive':ser['slope_end_pos'].values[0],'negative':ser['slope_end_neg'].values[0]}
    motor_obj = MotorCompensation(file_path,deadband_starts,deadband_ends,kinetic_coeffs,static_coeffs,slope_ends)
    motor_obj.plot_compensation()

def sign(num):
    if num > 0:
        return 1
    return -1

# Note this function throws an error for front 30, front 40, rear 20, rear 35 and rear 40 #
def find_constants(path,motor,speed):
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
    kinetic_coeffs = {'increasing':int((sum(neg_kinetic)/len(neg_kinetic))),'decreasing':int(sum(pos_kinetic)/len(pos_kinetic))}

    # Finding Static Coefficients in each direction by averaging #
    pos_static = [val for val in static_coeffs if val > 0]
    neg_static = [val for val in static_coeffs if val < 0]
    static_coeffs = {'decreasing':int((sum(neg_static)/len(neg_static))),'increasing':int(sum(pos_static)/len(pos_static))}

    # Print Statements to Check Values #
    print(f'{deadband_starts=}')
    print(f'{deadband_ends=}')
    print(f'{kinetic_coeffs=}')
    print(f'{static_coeffs=}')
    print(f'{slope_ends=}')

    # Print Statment in format of CSV File #
    print(f"{speed},{motor},{path},{deadband_starts[0]},{deadband_starts[1]},{deadband_starts[2]},{deadband_starts[3]},{deadband_ends[0]},{deadband_ends[1]},{deadband_ends[2]},{deadband_ends[3]},{kinetic_coeffs['increasing']},{kinetic_coeffs['decreasing']},{static_coeffs['increasing']},{static_coeffs['decreasing']},{slope_ends['positive']},{slope_ends['negative']}")
    
    # Calling Motor Object and Plotting #
    motor_obj = MotorCompensation(path,deadband_starts,deadband_ends,kinetic_coeffs,static_coeffs,slope_ends)
    motor_obj.plot_compensation()

def plot_raw(path):
    # Reading CSV into pandas DataFrame #
    df = pd.read_csv(path)
    df['Relative Time'] = df['Time']-df['Time'].iloc[0]
    print(df['Time'].iloc[0])

    # Plotting Angle vs Time #
    fig, axs = plt.subplots(2, 1)
    fig.set_figheight(8.5)
    fig.set_figwidth(14)

    # Plot on the first axis
    axs[0].plot(df['Relative Time'], df['Wheel Input'])
    axs[0].set_ylabel('Commanded Input (PWM Value)',fontsize=14)

    # Plot on the second axis
    axs[1].plot(df['Relative Time'], df['Wheel Speed'])
    axs[1].set_xlabel('Time (ms)',fontsize=14)
    axs[1].set_ylabel('Response (Degrees per Second)',fontsize=14)

    plt.show()

if __name__ == '__main__':
    # find_constants('./Python/deadband coeff/SourceData/RearSlope35Data.csv','rear',35)
    # plot_raw('./Python/deadband coeff/SourceData/RearSlope35Data.csv')

    # plot_motor_data(35,'rear')
    for i in range(1,11,1):
        # find_constants(f'./Python/deadband coeff/SourceData/FrontSlope{i}Data.csv','front',i)
        plot_motor_data(i,'front')
    
    for i in range(15,36,5):
        # find_constants(f'./Python/deadband coeff/SourceData/FrontSlope{i}Data.csv','front',i)
        plot_motor_data(i,'front')

    for i in range(1,11,1):
        # find_constants(f'./Python/deadband coeff/SourceData/RearSlope{i}Data.csv','rear',i)
        plot_motor_data(i,'rear')

    for i in range(15,36,5):
        # find_constants(f'./Python/deadband coeff/SourceData/RearSlope{i}Data.csv','rear',i)
        plot_motor_data(i,'rear')