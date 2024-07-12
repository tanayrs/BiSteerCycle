'''
Experiment: Dead Band Testing with 12bit PWM Resolution
By: Jia Bhargava, Tanay Srinivasa
Last Modified: 24 June 2024

Run bi_steer_cycle_testing arduino code with deadband_test()
'''

from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

class Motor:
    def __init__(self,path,deadband_starts, deadband_ends, deadband_inputs, slope_ends=None):
        self.df = pd.read_csv(path)
        self.df['Relative Time'] = self.df['Time']-self.df['Time'].iloc[0]
        
        # Correcting Bevel Gear Inaccuracy #
        try:
            self.df['Wheel Speed'] = 8*self.df['Wheel Speed']
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
        colors = ['tab:orange','tab:green']
        for index, input in enumerate(self.deadband_inputs):
            plt.axhline(y=input, color='k', linestyle='--', linewidth=0.5)
            plt.plot(self.deadband_ends[index],input,'o', color=colors[index], label='Deadband Exit for Decreasing Speed', ms=7.5)
            plt.plot(self.deadband_ends[index+2],input,'o', color=colors[index], label='Deadband Exit for Decreasing Speed', ms=7.5)

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
        colors = ['tab:orange','tab:green']
        for index,end in enumerate(self.deadband_ends):
            plt.axvline(x=end, color='k', linestyle='--', linewidth=0.5)
            plt.plot(end,0,'o', color=colors[index%2],ms=7.5)
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
        colors = ['tab:orange','tab:green']
        for input, color in zip(self.deadband_inputs,colors):
            plt.plot(input,0,'o',color=color,ms=10)
            plt.axvline(x=input, color='k', linestyle='--',linewidth=0.75)
        
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

def plot_front():
    path = './Python/deadband tests/deadband 12bit/SourceData/FrontUncompensatedData.csv'
    ends = [8174, 26449, 43525, 61378]
    inputs = [-170, 215]
    slope_ends = {'negative': 15234, 'positive': 32778}

    obj = Motor(path, [], ends, inputs, slope_ends)
    obj.plot_compensation()

def plot_rear():
    path = './Python/deadband tests/deadband 12bit/SourceData/RearUncompensatedData.csv'
    ends = [10279, 27891, 45383, 62937]
    inputs = [-160, 170]
    slope_ends = {'negative': 17289, 'positive': 34841}

    obj = Motor(path, [], ends, inputs, slope_ends)
    obj.plot_compensation()

def plot_front_compensated():
    path = './Python/deadband tests/deadband 12bit/SourceData/FrontCompensatedData.csv'
    ends = [10526, 28583, 45684, 63689]
    inputs = [-170, 215]
    slope_ends = {'negative': 17461, 'positive': 35008}

    obj = Motor(path, [], ends, inputs, slope_ends)
    obj.plot_compensation()

def plot_rear_compensated():
    path = './Python/deadband tests/deadband 12bit/SourceData/RearCompensatedData.csv'
    ends = [10520, 28132, 45625, 63293]
    inputs = [-160, 170]
    slope_ends = {'negative': 19359, 'positive': 36876}

    obj = Motor(path, [], ends, inputs, slope_ends)
    obj.plot_compensation()

if __name__ == '__main__':
    plot_front()
    plot_rear()
    plot_front_compensated()
    plot_rear_compensated()
