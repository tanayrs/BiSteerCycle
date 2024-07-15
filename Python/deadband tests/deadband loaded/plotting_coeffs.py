'''
Experiment: Finding Kinetic and Static Friction Coefficients
By: Jia Bhargava, Tanay Srinivasa
Last Modified: 1 Jul 2024

Run bi_steer_cycle_testing arduino code with deadband_test()
'''

from matplotlib import pyplot as plt
import pandas as pd

PLOTTING_CONSTANTS_PATH = './Python/deadband tests/deadband loaded/plotting_constants.csv'

x_front = [5,10,20]
x_rear = [5,10,20]

class MotorCompensation:
    # Constructor to Initialise Variables #
    def __init__(self, file_path, deadband_starts, deadband_ends, kinetic_coeffs, static_coeffs, slope_ends):
        self.df = pd.read_csv(file_path)
        self.df['Relative Time'] = self.df['Time']-self.df['Time'].iloc[0]
        self.df['Expected Response'] = self.df['Wheel Input'].apply(self.__calculate_expected_output)
        
        self.deadband_starts = deadband_starts
        self.deadband_ends = deadband_ends
        self.kinetic_coeffs = kinetic_coeffs
        self.static_coeffs = static_coeffs
        self.slope_ends = slope_ends

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
        subset = self.df[self.df['Relative Time']<=(self.df['Relative Time'].iloc[-1])/5]
        subset['Effective Input'] = subset['Wheel Speed'].apply(self.__calculate_effective_input)
        
        plt.plot(subset['Relative Time'], subset['Wheel Input'])
        # plt.plot(subset['Relative Time'], subset['Wheel Input'], label = 'Actual Input')
        # plt.plot(subset['Relative Time'], subset['Effective Input'], label = 'Effective Input')
        
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
        plt.plot(self.deadband_ends[0],self.static_coeffs['decreasing'],'o', color='tab:orange', label='Deadband Exit for Decreasing Speed', ms=7.5)
        plt.plot(self.deadband_ends[1],self.static_coeffs['increasing'],'o', color='tab:pink', label='Deadband Exit for Increasing Speed', ms=7.5)
        plt.plot(self.deadband_ends[2],self.static_coeffs['decreasing'],'o', color='tab:orange', ms=7.5)
        plt.plot(self.deadband_ends[3],self.static_coeffs['increasing'],'o', color='tab:pink', ms=7.5)

        plt.plot(self.deadband_starts[0],self.kinetic_coeffs['decreasing'],'o', color='tab:cyan', label='Deadband Entry for Decreasing Speed', ms=7.5)
        plt.plot(self.deadband_starts[1],self.kinetic_coeffs['increasing'],'o', color='tab:olive', label='Deadband Entry for Increasing Speed', ms=7.5)
        plt.plot(self.deadband_starts[2],self.kinetic_coeffs['decreasing'],'o', color='tab:cyan', ms=7.5)
        plt.plot(self.deadband_starts[3],self.kinetic_coeffs['increasing'],'o', color='tab:olive', ms=7.5)
        
        yticks = []
        set_continue = False
        deadband_inputs = [self.kinetic_coeffs['increasing'],self.kinetic_coeffs['decreasing'],self.static_coeffs['increasing'],self.static_coeffs['decreasing']]
        
        step = (self.df['Wheel Input'].max()-self.df['Wheel Input'].min())/7
        for i in range(int(self.df['Wheel Input'].min()),int(self.df['Wheel Input'].max()),int(step)):
            for input in deadband_inputs:
                if abs(i-input) < (self.df['Wheel Input'].max()-self.df['Wheel Input'].min())/14:
                    set_continue = True
            if set_continue == True:
                set_continue = False
                continue
            else:
                yticks.append(i)

        set_continue = False
        for input in deadband_inputs:
            for i in yticks:
                if i != input and abs(i-input) < (self.df['Wheel Input'].max()-self.df['Wheel Input'].min())/28:
                    set_continue = True
            if set_continue == True:
                set_continue = False
                continue
            else:
                yticks.append(input)

        # Adding Axis Labels, y-ticks and sub-plot title #
        plt.ylabel('Commanded Input (PWM Value)',fontsize=14)
        plt.xlabel('Time (ms)', fontsize=14)
        plt.yticks(yticks)
        plt.ylim([-820,820])
        plt.legend(loc='upper right', fontsize=12)
        plt.title('Input', fontsize=18)

    def __plot_output(self):
        subset = self.df[self.df['Relative Time']<=(self.df['Relative Time'].iloc[-1])/5]
        ### Command vs Time Plot ###
        plt.plot(subset['Relative Time'], subset['Wheel Speed'], label='Measured Response')
        plt.plot(subset['Relative Time'], subset['Expected Response'], label='Ideal Response', color='gray')

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
        plt.legend(loc='upper right', fontsize=14)
        plt.title('Measured and Ideal Response', fontsize=18)

        # plt.show()

    def __plot_cr_decreasing(self):
        plt.scatter(
            self.df[self.df['Relative Time']<= self.slope_ends['negative']]['Wheel Input'],
            self.df[self.df['Relative Time']<=self.slope_ends['negative']]['Wheel Speed'],
            label = 'Measured Response'
            )
        
        plt.scatter(
            self.df[self.df['Relative Time']<= self.slope_ends['negative']]['Wheel Input'],
            self.df[self.df['Relative Time']<=self.slope_ends['negative']]['Expected Response'],
            color = 'gray',
            s=10,
            label = 'Ideal Response'
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
        plt.xlim([-400,400])
        plt.ylim([-self.df['Wheel Speed'].max()/3,self.df['Wheel Speed'].max()/3])
        plt.ylabel('Response (Degrees Per Second)', fontsize=14)
        plt.legend(fontsize=14)
        plt.title('Commanded Input vs Response for Reducing Speed', fontsize=18)

    def __plot_cr_increasing(self):
        # time = self.df[self.df['Relative Time']>=self.slope_ends['negative']]
        # time = time[time['Relative Time']<=self.slope_ends['positive']]
        subset = self.df[self.df['Relative Time']>=self.slope_ends['negative']]
        subset = subset[subset['Relative Time']<=self.slope_ends['positive']]
        plt.scatter(subset['Wheel Input'],subset['Wheel Speed'], label='Measured Response')
        plt.scatter(subset['Wheel Input'],subset['Expected Response'],color='gray',s=10,label='Ideal Response')
        
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
        plt.legend(loc='upper left',fontsize=14)
        plt.title('Commanded Input vs Response for Increasing Speed', fontsize=18)

    def __plot_cr_combined(self):
        subset = self.df[self.df['Relative Time']>=self.slope_ends['negative']]
        subset = subset[subset['Relative Time']<=self.slope_ends['positive']]
    
        plt.scatter(
            subset['Wheel Input'],
            subset['Wheel Speed'], 
            label='Measured Inc Response', 
            marker='^',
            color='tab:green',
            s=25,
            linewidths=1.75
            )
        
        plt.scatter(
            self.df[self.df['Relative Time']<= self.slope_ends['negative']]['Wheel Input'],
            self.df[self.df['Relative Time']<=self.slope_ends['negative']]['Wheel Speed'],
            label = 'Measured Dec Response',
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
        plt.axvline(x=self.static_coeffs['decreasing'], color='k', linestyle='--',linewidth=0.75)
        plt.axvline(x=self.kinetic_coeffs['decreasing'], color='k', linestyle='--',linewidth=0.75)
        plt.axvline(x=self.static_coeffs['increasing'], color='k', linestyle='--',linewidth=0.75)
        plt.axvline(x=self.kinetic_coeffs['increasing'], color='k', linestyle='--',linewidth=0.75)
        
        # Plotting Horizontal Line to Demarkate Line for No Response Speed #
        plt.axhline(y=0, color='k',linestyle='--',linewidth=0.75)
        
        # Plotting Points at which Static and Kinetic Coefficients are Measured #
        plt.plot(self.static_coeffs['decreasing'],0,'o',color='tab:orange',ms=10)
        plt.plot(self.kinetic_coeffs['decreasing'],0,'o',color='tab:cyan', ms=10)
        plt.plot(self.static_coeffs['increasing'],0,'o',color='tab:pink', ms=10)
        plt.plot(self.kinetic_coeffs['increasing'],0,'o',color='tab:olive', ms=10)
        
        # Calculating Ticks #
        xticks = []
        set_continue = False

        deadband_inputs = [self.kinetic_coeffs['increasing'],self.kinetic_coeffs['decreasing'],self.static_coeffs['increasing'],self.static_coeffs['decreasing']]
        
        step = (self.df['Wheel Input'].max()-self.df['Wheel Input'].min())/7
        for i in range(int(self.df['Wheel Input'].min()),int(self.df['Wheel Input'].max()),int(step)):
            for input in deadband_inputs:
                if abs(i-input) < (self.df['Wheel Input'].max()-self.df['Wheel Input'].min())/14:
                    set_continue = True
            if set_continue == True:
                set_continue = False
                continue
            else:
                xticks.append(i)

        set_continue = False
        for input in deadband_inputs:
            for i in xticks:
                if i != input and abs(i-input) < (self.df['Wheel Input'].max()-self.df['Wheel Input'].min())/42:
                    set_continue = True
            if set_continue == True:
                set_continue = False
                continue
            else:
                xticks.append(input)

        xticks[-1] = self.df['Wheel Input'].max()

        # Setting x-ticks, axese limits, axese labels and sub-plot title #
        plt.xticks(xticks)
        plt.xlim([-400,400])
        plt.ylim([-self.df['Wheel Speed'].max()/3,self.df['Wheel Speed'].max()/3])
        plt.ylabel('Response (Degrees Per Second)', fontsize=14)
        plt.legend(fontsize=12)
        plt.legend(loc='upper left',fontsize=14)
        plt.title('Commanded Input vs Response', fontsize=18)

    def __calculate_expected_output(self,pwm):
        PWM_RESOLUTION = 4095
        MOTOR_RPM = 587
        ratio = pwm/PWM_RESOLUTION
        expected_speed = (MOTOR_RPM/60)* ratio * 360
        return expected_speed

    def __calculate_effective_input(self,speed):
        PWM_RESOLUTION = 4095
        MOTOR_RPM = 587
        effective_input = (60/MOTOR_RPM)*PWM_RESOLUTION*(1/360)*speed
        return effective_input

def plot_motor_data(motor,speed):
    file_path = f'./Python/deadband tests/deadband loaded/SourceData/{motor}Slope{speed}Data.csv'
    plot_constants_path = f'./Python/deadband tests/deadband loaded/PlottingConstants/{motor}Slope{speed}Constants.csv'
    slope_ends_path = './Python/deadband tests/deadband loaded/SlopeEnds.csv'
    
    df = pd.read_csv(plot_constants_path)
    
    slope_df = pd.read_csv(slope_ends_path)
    ser = slope_df.loc[(slope_df['speed']==speed) & (slope_df['motor']==motor)]
    
    starts = [df['deadband_starts_dec'].iloc[0],df['deadband_starts_inc'].iloc[0],df['deadband_starts_dec'].iloc[1],df['deadband_starts_inc'].iloc[1]]
    ends = [df['deadband_ends_dec'].iloc[0],df['deadband_ends_inc'].iloc[0],df['deadband_ends_dec'].iloc[1],df['deadband_ends_inc'].iloc[1]]

    kinetic = {'increasing':df['kinetic_coeffs_inc'].mean(),'decreasing':df['kinetic_coeffs_dec'].mean()}
    static = {'increasing':df['static_coeffs_inc'].mean(), 'decreasing':df['static_coeffs_dec'].mean()}
    
    slope_ends = {'positive':ser['positive'].values[0],'negative':ser['negative'].values[0]}
    
    print(f'{file_path=}\n{starts=}\n{ends=}\n{kinetic=}\n{static=}\n{slope_ends=}',end='\n\n')

    motor_obj = MotorCompensation(file_path,starts,ends,kinetic,static,slope_ends)
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
    # find_constants('./Python/deadband tests/deadband coeff/SourceData/RearSlope35Data.csv','rear',35)
    # plot_raw('./deadband tests/Python/deadband coeff/SourceData/RearSlope35Data.csv')

    # plot_motor_data('Rear',10)
    plot_compensation('Front',5)
    
    # plot_motor_data(5,'rear')
    # for i in range(1,11,1):
    #     find_constants(f'./Python/deadband tests/deadband coeff/SourceData/FrontSlope{i}Data.csv','front',i)
    #     # plot_motor_data(i,'front')
    
    # for i in range(15,36,5):
    #     find_constants(f'./Python/deadband tests/deadband coeff/SourceData/FrontSlope{i}Data.csv','front',i)
    #     # plot_motor_data(i,'front')

    # for i in range(1,11,1):
    #     find_constants(f'./Python/deadband tests/deadband coeff/SourceData/RearSlope{i}Data.csv','rear',i)
    #     # plot_motor_data(i,'rear')

    # for i in range(15,36,5):
    #     find_constants(f'./Python/deadband tests/deadband coeff/SourceData/RearSlope{i}Data.csv','rear',i)
    #     # plot_motor_data(i,'rear')