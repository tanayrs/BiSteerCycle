'''
Experiment: Dead Band Testing
By: Jia Bhargava, Tanay Srinivasa
Last Modified: 20 June 2024

Run bi_steer_cycle arduino code with set_dead_band_speed()
'''

from matplotlib import pyplot as plt
import pandas as pd

class Motor:
    def __init__(self, path, ends, inputs):
        self.df = pd.read_csv(path)
        self.df['Relative Time'] = self.df['Time']-self.df['Time'].iloc[0]

        self.deadband_ends = ends
        self.deadband_inputs = inputs

    def plot(self):
        # Plotting Angle vs Time #
        fig, axs = plt.subplots(2, 1)
        fig.set_figheight(8.5)
        fig.set_figwidth(14)

        # Plot on the first axis
        axs[0].plot(self.df['Relative Time'], self.df['Wheel Input'])
        for end in self.deadband_ends:
            axs[0].axvline(x=end, color='k', linestyle='--', linewidth=0.5)
        
        for input in self.deadband_inputs:
            axs[0].axhline(y=input, color='k', linestyle='--', linewidth=0.5)
        
        try:
            axs[0].plot(self.deadband_ends[0],self.deadband_inputs[0],'o')
            axs[0].plot(self.deadband_ends[1],self.deadband_inputs[1],'o')
            axs[0].plot(self.deadband_ends[2],self.deadband_inputs[0],'o')
            axs[0].plot(self.deadband_ends[3],self.deadband_inputs[1],'o')
        except:
            pass
        
        # axs[0].set_ylabel('Commanded Input (PWM Value)',fontsize=14)
        axs[0].set_ylabel('Input (PWM)',fontsize=28)
        axs[0].set_yticks([-50,-40,-30,-20,-11,-5,5,11,20,30,40,50])
        axs[0].set_xticks([])

        # Plot on the second axis
        axs[1].plot(self.df['Relative Time'], self.df['Wheel Speed'])
        for end in self.deadband_ends:
            axs[1].axvline(x=end, color='k', linestyle='--', linewidth=0.5)
            axs[1].plot(end,0,'o')
        
        axs[1].set_xlabel('Time (ms)',fontsize=28)
        # axs[1].set_ylabel('Response (Degrees per Second)',fontsize=14)
        axs[1].set_ylabel('Response (d/s)',fontsize=28)

        # Show the plot
        plt.tight_layout()
        plt.show()

        sorted_df = self.df.sort_values('Wheel Input')
        plt.scatter(sorted_df['Wheel Input'],sorted_df['Wheel Speed'])
        # plt.xlabel('Commanded Value (PWM Input)', fontsize=28)
        # plt.ylabel('Response (Degrees Per Second)', fontsize=28)
        plt.xlabel('Input (PWM)', fontsize=28)
        plt.ylabel('Response (d/s)', fontsize=28)
        # plt.title('Commanded Value vs Response')
        plt.show()

def plot_front():
    path = './Python/deadband tests/deadband 8bit/SourceData/TriangleFrontDeadBandDataSpeed.csv'
    ends = [12253, 33382, 54837, 75752]
    inputs = [-11, 11]
    
    obj = Motor(path, ends, inputs)
    obj.plot()

def plot_rear():
    path = './Python/deadband tests/deadband 8bit/SourceData/TriangleRearDeadBandDataSpeedUnscaled.csv'
    ends = [253569 - 240536, 274913 - 240536, 2.9550e+05 - 240536, 3.1726e+05 - 240536]
    inputs = [-9, 11]

    obj = Motor(path, ends, inputs)
    obj.plot()

def plot_front_compensated():
    path = 'Python/deadband tests/deadband 8bit/SourceData/TriangleFrontDeadBandDataSpeedCorrected_5.csv'
    ends = []
    inputs = []
    obj = Motor(path, ends, inputs)
    obj.plot()

def plot_rear_compensated():
    path = 'Python/deadband tests/deadband 8bit/SourceData/TriangleRearDeadBandDataSpeedCorrected_3.csv'
    obj = Motor(path,[],[])
    obj.plot()

if __name__ == '__main__':
    # plot_front()
    # plot_rear()
    # plot_front_compensated()
    plot_rear_compensated()