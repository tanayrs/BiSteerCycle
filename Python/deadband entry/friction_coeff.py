'''
Experiment: Finding Kinetic and Static Friction Coefficients
By: Jia Bhargava, Tanay Srinivasa
Last Modified: 30 June 2024

Run bi_steer_cycle_testing arduino code with deadband_test()
'''

from matplotlib import pyplot as plt
import pandas as pd

class MotorCompensation:
    def __init__(self, file_path, deadband_starts, deadband_ends, kinetic_coeffs, static_coeffs, slope_ends):
        self.df = pd.read_csv(file_path)
        self.df['Relative Time'] = self.df['Time']-self.df['Time'].iloc[0]
        self.df['Wheel Speed Corrected'] = self.df['Wheel Speed']*8
        
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
        self.df['Effective Input'] = self.df['Wheel Speed Corrected'].apply(self.__calculate_effective_input)
        plt.plot(self.df['Relative Time'], self.df['Wheel Input'])
        # plt.plot(self.df['Relative Time'], self.df['Wheel Input'], label = 'Actual Input')
        # plt.plot(df['Relative Time'], df['Effective Input'], label = 'Effective Input')
        
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
        plt.yticks([-800,-600,-400,-170,0,self.kinetic_coeffs['decreasing'],215,400,600,800])
        plt.ylim([-820,820])
        plt.legend(loc='upper right', fontsize=14)
        plt.title('Input', fontsize=14)

    def __plot_output(self):
        self.df['Expected Response'] = self.df['Wheel Input'].apply(self.__calculate_expected_output)
        self.df['Wheel Speed Corrected'] = self.df['Wheel Speed']*8
        
        ### Command vs Time Plot ###
        plt.plot(self.df['Relative Time'], self.df['Wheel Speed Corrected'], label='Actual Response')
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
        plt.ylim([-30,30])
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
        plt.ylim([-30,30])
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

plotting_constants_path = './Python/deadband entry/plotting_constants.csv'
def plot_motor(speed,motor):
    df = pd.read_csv(plotting_constants_path)
    ser = df[df['speed']==speed]
    ser = ser[ser['motor']==motor]
    file_path = ser['path']
    deadband_starts = [ser['deadband_start1'], ser['deadband_start2'], ser['deadband_start3'], ser['deadband_start4']]
    deadband_ends = [ser['deadband_end1'], ser['deadband_end2'], ser['deadband_end3'], ser['deadband_end4']]
    kinetic_coeffs = {'increasing':ser['kinetic_coeff_inc'],'decreasing':ser['kinetic_coeff_dec']}
    static_coeffs = {'increasing': ser['static_coeff_inc'], 'decreasing':ser['static_coeff_dec']}
    slope_ends = {'positive':ser['slope_end_pos'],'negative':ser['slope_end_neg']}
    print(f'{file_path=}')
    print(f'{deadband_ends=}')
    print(f'{deadband_starts=}')
    print(f'{kinetic_coeffs=}')
    print(f'{static_coeffs=}')
    print(f'{slope_ends=}')
    # front_motor_obj = MotorCompensation(file_path,desadband_starts,deadband_ends,kinetic_coeffs,static_coeffs,slope_ends)
    # front_motor_obj.plot_compensation()

def plot_front_motor_10():
    file_path = './Python/deadband entry/SourceData/FrontSlope10Data.csv'
    deadband_starts = [5066, 22488, 40158, 57770]
    deadband_ends = [8174, 26449, 43525, 61378]
    kinetic_coeffs = {'increasing':-135,'decreasing':130}
    static_coeffs = {'increasing': 215, 'decreasing':-170}
    slope_ends = {'positive':32759,'negative':15209}
    front_motor_obj = MotorCompensation(file_path,deadband_starts,deadband_ends,kinetic_coeffs,static_coeffs,slope_ends)
    front_motor_obj.plot_compensation()

def plot_rear_motor_10():
    file_path = './Python/deadband entry/SourceData/RearSlope10Data.csv'
    deadband_starts = [7341, 24766,42319,59875]
    deadband_ends = [10279,27891,45383,62937]
    kinetic_coeffs = {'increasing':-120,'decreasing':115}
    static_coeffs = {'increasing': 170, 'decreasing':-160}
    slope_ends = {'positive':34748,'negative':17317}
    rear_motor_obj = MotorCompensation(file_path,deadband_starts,deadband_ends,kinetic_coeffs,static_coeffs,slope_ends)
    rear_motor_obj.plot_compensation()

def plot_front_motor_20():
    file_path = './Python/deadband entry/SourceData/FrontSlope20Data.csv'

    # Input Value Corresponding to Deadband #
    deadband_starts = [3668, 12502, 21278, 30115]
    deadband_ends = [5235, 14070, 22849, 31555]
    kinetic_coeffs = {'increasing':-110,'decreasing':120}
    static_coeffs = {'increasing': 215, 'decreasing':-170}
    slope_ends = {'positive':17619,'negative':8779}
    front_motor_obj = MotorCompensation(file_path,deadband_starts,deadband_ends,kinetic_coeffs,static_coeffs,slope_ends)
    front_motor_obj.plot_compensation()

def plot_rear_motor_20():
    file_path = './Python/deadband entry/SourceData/RearSlope20Data.csv'
    deadband_starts = [3846, 12743, 21642, 30476]
    deadband_ends = [5279, 14190, 23083, 31737]
    kinetic_coeffs = {'increasing':-100,'decreasing':100}
    static_coeffs = {'increasing': 170, 'decreasing':-160}
    slope_ends = {'positive':17735,'negative':8959}
    rear_motor_obj = MotorCompensation(file_path,deadband_starts,deadband_ends,kinetic_coeffs,static_coeffs,slope_ends)
    rear_motor_obj.plot_compensation()

def plot_front_motor_40():
    file_path = './Python/deadband entry/SourceData/FrontSlope40Data.csv'

    # Input Value Corresponding to Deadband #
    deadband_starts = [1983, 6312, 10880, 15268]
    deadband_ends = [2585, 7093, 11425, 15989]
    kinetic_coeffs = {'increasing':-90,'decreasing':70}
    static_coeffs = {'increasing': 215, 'decreasing':-170}
    slope_ends = {'positive':8849,'negative':4451}
    front_motor_obj = MotorCompensation(file_path,deadband_starts,deadband_ends,kinetic_coeffs,static_coeffs,slope_ends)
    front_motor_obj.plot_compensation()

def plot_rear_motor_40():
    file_path = './Python/deadband entry/SourceData/RearSlope40Data.csv'
    deadband_starts = [1924, 6552, 11065, 15685]
    deadband_ends = [2710, 7273, 11781, 16350]
    kinetic_coeffs = {'increasing':-80,'decreasing':90}
    static_coeffs = {'increasing': 170, 'decreasing':-160}
    slope_ends = {'positive':9078,'negative':4574}
    rear_motor_obj = MotorCompensation(file_path,deadband_starts,deadband_ends,kinetic_coeffs,static_coeffs,slope_ends)
    rear_motor_obj.plot_compensation()

if __name__ == '__main__':
    # plot_front_motor_10()
    # plot_rear_motor_10()
    # plot_front_motor_20()
    # plot_rear_motor_20()
    # plot_front_motor_40()
    # plot_rear_motor_40()
    plot_motor(10,"front")