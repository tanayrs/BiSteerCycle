'''
Experiment: Plotting Compensation after using the Kinetic and Static Friction Coefficients
By: Jia Bhargava, Tanay Srinivasa
Last Modified: 1 Jul 2024

Run bi_steer_cycle_testing arduino code with deadband_test()
'''

from matplotlib import pyplot as plt
import pandas as pd

PLOTTING_CONSTANTS_PATH = './Python/deadband coeff/plotting_constants.csv'

class MotorCompensation:
    def __init__(self, comp_file_path, uncomp_file_path,deadband_starts, deadband_ends, kinetic_coeffs, static_coeffs, slope_ends, slope_ends_uncomp):
        self.df = pd.read_csv(comp_file_path)
        self.df_uncomp = pd.read_csv(uncomp_file_path)
        self.df['Relative Time'] = self.df['Time']-self.df['Time'].iloc[0]
        self.df_uncomp['Relative Time'] = self.df_uncomp['Time']-self.df_uncomp['Time'].iloc[0]
        self.df['Expected Response'] = self.df['Wheel Input'].apply(self.__calculate_expected_output)
        
        self.deadband_starts = deadband_starts
        self.deadband_ends = deadband_ends
        self.kinetic_coeffs = kinetic_coeffs
        self.static_coeffs = static_coeffs
        self.slope_ends = slope_ends
        self.slope_ends_uncomp = slope_ends_uncomp

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
        # plt.vlines(x=self.deadband_ends[0], ymin=-900, ymax=self.static_coeffs['decreasing'], color='k', linestyle='--', linewidth=0.5)
        # plt.vlines(x=self.deadband_ends[1], ymin=-900, ymax=self.static_coeffs['increasing'], linestyle='--', linewidth=0.5)
        # plt.vlines(x=self.deadband_ends[2], ymin=-900, ymax=self.static_coeffs['decreasing'], color='k', linestyle='--', linewidth=0.5)
        # plt.vlines(x=self.deadband_ends[3], ymin=-900,ymax=self.static_coeffs['increasing'], color='k', linestyle='--', linewidth=0.5)
        # plt.vlines(x=self.deadband_starts[0], ymin=-900, ymax=self.kinetic_coeffs['decreasing'], color='k', linestyle='--', linewidth=0.5)
        # plt.vlines(x=self.deadband_starts[1], ymin=-900, ymax=self.kinetic_coeffs['increasing'], color='k', linestyle='--', linewidth=0.5)
        # plt.vlines(x=self.deadband_starts[2], ymin=-900, ymax=self.kinetic_coeffs['decreasing'], color='k', linestyle='--', linewidth=0.5)
        # plt.vlines(x=self.deadband_starts[3], ymin=-900, ymax=self.kinetic_coeffs['increasing'], color='k', linestyle='--', linewidth=0.5)
        
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
        total_speed_error = self.df['Expected Response']-self.df['Wheel Speed']
        print(f'{total_speed_error.sum()/len(self.df)=}')
        ### Command vs Time Plot ###
        plt.plot(self.df['Relative Time'], self.df['Expected Response'], label='Expected Response', color='saddlebrown',linewidth=1.75)
        # plt.plot(self.df_uncomp['Relative Time'], self.df_uncomp['Wheel Speed'], color='gray', linewidth=1, label='Uncompensated Response')
        plt.plot(self.df['Relative Time'], self.df['Wheel Speed'], label='Compensated Response')

        # Plotting Vertical Dotted Lines for Start and End of Deadband #
        # plt.vlines(x=self.deadband_ends[0], ymin=0, ymax=800, color='k', linestyle='--', linewidth=0.5)
        # plt.vlines(x=self.deadband_ends[1], ymin=0, ymax=800, color='k', linestyle='--', linewidth=0.5)
        # plt.vlines(x=self.deadband_ends[2], ymin=0, ymax=800, color='k', linestyle='--', linewidth=0.5)
        # plt.vlines(x=self.deadband_ends[3], ymin=0, ymax=800, color='k', linestyle='--', linewidth=0.5)
        # plt.vlines(x=self.deadband_starts[0], ymin=0, ymax=800, color='k', linestyle='--', linewidth=0.5)
        # plt.vlines(x=self.deadband_starts[1], ymin=0, ymax=800, color='k', linestyle='--', linewidth=0.5)
        # plt.vlines(x=self.deadband_starts[2], ymin=0, ymax=800, color='k', linestyle='--', linewidth=0.5)
        # plt.vlines(x=self.deadband_starts[3], ymin=0, ymax=800, color='k', linestyle='--', linewidth=0.5)

        # plt.axhline(y=0, color='k', linestyle='--', linewidth=0.5)
        
        # Plotting Colored Dots Corresponding to the Static and Kinetic Coefficients #
        # plt.plot(self.deadband_ends[0],0,'o', color='tab:orange', ms=7.5)
        # plt.plot(self.deadband_ends[1],0,'o', color='tab:pink', ms=7.5)
        # plt.plot(self.deadband_ends[2],0,'o', color='tab:orange', ms=7.5)
        # plt.plot(self.deadband_ends[3],0,'o', color='tab:pink', ms=7.5)
        # plt.plot(self.deadband_starts[0],0,'o', color='tab:cyan', ms=7.5)
        # plt.plot(self.deadband_starts[1],0,'o', color='tab:olive', ms=7.5)
        # plt.plot(self.deadband_starts[2],0,'o', color='tab:cyan', ms=7.5)
        # plt.plot(self.deadband_starts[3],0,'o', color='tab:olive', ms=7.5)
        
        # Plotting Axis Labels and Sub-Plot Title #
        plt.xlabel('Time (ms)',fontsize=14)
        plt.ylabel('Response (Degrees per Second)',fontsize=14)
        plt.ylim([-720,720])
        plt.legend(loc='upper right',fontsize=14)
        plt.title('Expected and Actual Response', fontsize=14)

        # plt.show()

    def __plot_cr_decreasing(self):
        plt.scatter(
            self.df_uncomp[self.df_uncomp['Relative Time']<= self.slope_ends_uncomp['negative']]['Wheel Input'],
            self.df_uncomp[self.df_uncomp['Relative Time']<=self.slope_ends_uncomp['negative']]['Wheel Speed'],
            color='gray',
            marker='o',
            label='Uncompensated Points',
            s=20
        )

        # plt.scatter(self.df['Wheel Input'], self.df['Expected Response'], color='gray', label='Ideal Compensation')

        plt.scatter(
            self.df[self.df['Relative Time']<= self.slope_ends['negative']]['Wheel Input'],
            self.df[self.df['Relative Time']<=self.slope_ends['negative']]['Wheel Speed'],
            label='Compensated Points'
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
        plt.legend(fontsize=14)
        plt.title('Deadband Static Coefficient for Reducing Speed', fontsize=14)

    def __plot_cr_increasing(self):
        comp_subset = self.df.loc[(self.df['Relative Time']>=self.slope_ends['negative']) & (self.df['Relative Time']<=self.slope_ends['positive'])]
        uncomp_subset = self.df_uncomp.loc[(self.df_uncomp['Relative Time']>=self.slope_ends_uncomp['negative']) & (self.df_uncomp['Relative Time']<=self.slope_ends_uncomp['positive'])]

        plt.scatter(uncomp_subset['Wheel Input'], uncomp_subset['Wheel Speed'], color='gray', marker='o', label='Uncompensated Points', s=20)

        # plt.scatter(self.df['Wheel Input'], self.df['Expected Response'], color='gray', label='Ideal Compensation')
        
        plt.scatter(comp_subset['Wheel Input'], comp_subset['Wheel Speed'], label='Compensated Points')
        
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
        plt.legend(fontsize=14)
        plt.title('Deadband Static Coefficient for Increasing Speed', fontsize=14)

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

def plot_motor_data(speed,motor):
    # Loading Dataframe Containing Plotting Constants #
    df = pd.read_csv(PLOTTING_CONSTANTS_PATH)

    # Loading series with compensated and uncompensated constants #
    ser = df.loc[(df['speed']==speed) & (df['motor']==motor) & (df['comp']=='comp')]
    uncomp_ser = df.loc[(df['speed']==speed) & (df['motor']==motor) & (df['comp']=='uncomp')]

    # Finding filepaths for compensated and uncompensated data #
    comp_file_path = ser['path'].values[0]
    uncomp_file_path = uncomp_ser['path'].values[0]
    
    # Loading times where the deadband starts and ends for the uncompensated data #
    deadband_starts = [ser['deadband_start1'].values[0], ser['deadband_start2'].values[0], ser['deadband_start3'].values[0], ser['deadband_start4'].values[0]]
    deadband_ends = [ser['deadband_end1'].values[0], ser['deadband_end2'].values[0], ser['deadband_end3'].values[0], ser['deadband_end4'].values[0]]
    
    # Loading Input corresponding to deadband entry and exist for the motor #
    kinetic_coeffs = {'increasing':ser['kinetic_coeff_inc'].values[0],'decreasing':ser['kinetic_coeff_dec'].values[0]}
    static_coeffs = {'increasing': ser['static_coeff_inc'].values[0], 'decreasing':ser['static_coeff_dec'].values[0]}
    
    # Finding Time at which the first slope in the positive and negative direction ends #
    slope_ends = {'positive':ser['slope_end_pos'].values[0],'negative':ser['slope_end_neg'].values[0]}
    slope_ends_uncomp = {'positive':uncomp_ser['slope_end_pos'].values[0],'negative':uncomp_ser['slope_end_neg'].values[0]}
    
    # Creating a motor object and plotting #
    motor_obj = MotorCompensation(comp_file_path, uncomp_file_path,deadband_starts, deadband_ends, kinetic_coeffs, static_coeffs, slope_ends, slope_ends_uncomp)
    motor_obj.plot_compensation()

if __name__ == '__main__':
    plot_motor_data(10,'front')