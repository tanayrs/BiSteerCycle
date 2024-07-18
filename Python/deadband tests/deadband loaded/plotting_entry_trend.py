'''
Experiment: Plotting kinetic deadband coefficients for different slopes with error bars
By: Jia Bhargava, Tanay Srinivasa
Last Modified: 3 Jul 2024
'''

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

class ErrorTrend:
    def __init__(self, x_loaded, x_unloaded):
        self.x_loaded =x_loaded
        self.x_unloaded =x_unloaded

        front_unloaded_tuple = self.__find_errors_unloaded("Front")
        self.front_unloaded = {'y_inc': front_unloaded_tuple[0], 'y_dec': front_unloaded_tuple[1], 'y_min': front_unloaded_tuple[2], 'y_max': front_unloaded_tuple[3], 'err_inc': front_unloaded_tuple[4], 'err_dec': front_unloaded_tuple[5]}
        
        rear_unloaded_tuple = self.__find_errors_unloaded("Rear")
        self.rear_unloaded = {'y_inc': rear_unloaded_tuple[0], 'y_dec': rear_unloaded_tuple[1], 'y_min': rear_unloaded_tuple[2], 'y_max': rear_unloaded_tuple[3], 'err_inc': rear_unloaded_tuple[4], 'err_dec': rear_unloaded_tuple[5]}
        
        front_loaded_tuple = self.__find_errors_loaded("Front")
        self.front_loaded = {'y_inc': front_loaded_tuple[0], 'y_dec': front_loaded_tuple[1], 'y_min': front_loaded_tuple[2], 'y_max': front_loaded_tuple[3], 'err_inc': front_loaded_tuple[4], 'err_dec': front_loaded_tuple[5]}
        
        rear_loaded_tuple = self.__find_errors_loaded("Rear")
        self.rear_loaded = {'y_inc': rear_loaded_tuple[0], 'y_dec': rear_loaded_tuple[1], 'y_min': rear_loaded_tuple[2], 'y_max': rear_loaded_tuple[3], 'err_inc': rear_loaded_tuple[4], 'err_dec': rear_loaded_tuple[5]}

    
    def __find_errors_loaded(self,motor):
        y_inc = []
        y_dec = []
        y_min = []
        y_max = []
        err_inc = []
        err_dec = []

        for i in x_loaded:
            path = f'./Python/deadband tests/deadband loaded/PlottingConstants/{motor}Slope{i}Constants.csv'
            df = pd.read_csv(path)
            y_inc.append(df['kinetic_coeffs_inc'].mean())
            y_dec.append(df['kinetic_coeffs_dec'].mean())
            y_min.append(df['kinetic_coeffs_inc'].min())
            y_max.append(df['kinetic_coeffs_dec'].max())
            err_inc.append(abs(df['kinetic_coeffs_inc'].std()))
            err_dec.append(abs(df['kinetic_coeffs_dec'].std()))

        return (y_inc, y_dec, y_min, y_max, err_inc, err_dec)

    def __find_errors_unloaded(self, motor):
        y_inc = []
        y_dec = []
        y_min = []
        y_max = []
        err_inc = []
        err_dec = []

        for i in x_unloaded:
            path = f'./Python/deadband tests/deadband coeff/plot constants/CombinedConstants/{motor}Slope{i}Constants.csv'
            df = pd.read_csv(path)
            y_inc.append(df['kinetic_coeffs_inc'].mean())
            y_dec.append(df['kinetic_coeffs_dec'].mean())
            y_min.append(df['kinetic_coeffs_inc'].min())
            y_max.append(df['kinetic_coeffs_dec'].max())
            err_inc.append(abs(df['kinetic_coeffs_inc'].std()))
            err_dec.append(abs(df['kinetic_coeffs_dec'].std()))

        return (y_inc, y_dec, y_min, y_max, err_inc, err_dec)

    def plot_subplot(self, loaded_dict, unloaded_dict, type, label):
        if type == 'Inc':
            plt.errorbar(self.x_loaded, loaded_dict['y_inc'], loaded_dict['err_inc'], label='Loaded Measurement', capsize=5)
            plt.scatter(self.x_loaded, loaded_dict['y_inc'])
            
            plt.errorbar(self.x_unloaded, unloaded_dict['y_inc'], unloaded_dict['err_inc'], label='Unloaded Measurement', capsize=5, color = 'gray')
            plt.scatter(self.x_unloaded, unloaded_dict['y_inc'], color = 'gray')
            
            if max(loaded_dict['y_min']) > 0:
                plt.ylim([0, max(loaded_dict['y_min'])])
            else:
                plt.ylim([min(loaded_dict['y_min']),0])
        else:
            plt.errorbar(self.x_loaded, loaded_dict['y_dec'], loaded_dict['err_dec'], label='Loaded Measurement', capsize=5)
            plt.scatter(self.x_loaded, loaded_dict['y_dec'])
            
            plt.errorbar(self.x_unloaded, unloaded_dict['y_dec'], unloaded_dict['err_dec'], label='Unloaded Measurement', capsize=5, color = 'gray')
            plt.scatter(self.x_unloaded, unloaded_dict['y_dec'], color = 'gray')
            
            if max(loaded_dict['y_max']) > 0:
                plt.ylim([0, max(loaded_dict['y_max'])])
            else:
                plt.ylim([min(loaded_dict['y_max']),0])
            
        plt.xticks(x_unloaded)
        plt.grid()
        plt.legend(fontsize=14)
        plt.title(label,fontsize=18)
        plt.xlabel('Slope of Input Speed (PWM per 100ms)',fontsize=14)
        plt.ylabel('Deadband Value (PWM)',fontsize=14)
    
    def plot_errors(self):
        plt.subplot(2,2,1)
        self.plot_subplot(self.front_loaded,self.front_unloaded,'Inc','Front Deadband for Increasing Speed')

        plt.subplot(2,2,2)
        self.plot_subplot(self.front_loaded,self.front_unloaded,'Dec','Front Deadband for Decreasing Speed')

        plt.subplot(2,2,3)
        self.plot_subplot(self.rear_loaded,self.rear_unloaded,'Inc','Rear Deadband for Increasing Speed')

        plt.subplot(2,2,4)
        self.plot_subplot(self.rear_loaded,self.rear_unloaded,'Dec','Rear Deadband for Decreasing Speed')

        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle()
        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    # plot_trend_avg
    x_loaded = [5,10,20]
    x_unloaded = [2,3,4,5,6,7,8,9,10,15,20,25,30,35,40]
    obj = ErrorTrend(x_loaded, x_unloaded)
    obj.plot_errors()