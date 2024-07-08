'''
Experiment: Plotting kinetic deadband coefficients for different slopes with error bars
By: Jia Bhargava, Tanay Srinivasa
Last Modified: 3 Jul 2024
'''

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

x_front = [2,3,4,5,6,7,8,9,10,15,20,25,30,35,40]
x_rear = [2,3,4,5,6,7,8,9,10,15,20,25,30,35,40]

def find_errors(motor):
    y_inc = []
    y_dec = []
    err_inc = []
    err_dec = []

    if motor == "Front":
        x = x_front
    else:
        x = x_rear

    for i in x:
        path = f'./Python/deadband tests/deadband coeff/plot constants/CombinedConstants/{motor}Slope{i}Constants.csv'
        df = pd.read_csv(path)
        y_inc.append(df['kinetic_coeffs_inc'].mean())
        y_dec.append(df['kinetic_coeffs_dec'].mean())
        err_inc.append(abs(df['kinetic_coeffs_inc'].std()))
        err_dec.append(abs(df['kinetic_coeffs_dec'].std()))

    return (y_inc, y_dec, err_inc, err_dec)

def plot_subplot(x, y, err, label):
    plt.errorbar(x, y, err, label=label, capsize=5)
    plt.scatter(x, y)
    plt.xlabel('Slope of Input Speed (PWM per 100ms)',fontsize=14)
    plt.ylabel('Deadband Value (PWM)',fontsize=14)
    plt.xticks([1,2,3,4,5,6,7,8,9,10,15,20,25,30,35])
    plt.grid()
    plt.title(label,fontsize=18)
    
def plot_errors():
    y_front_inc, y_front_dec, err_front_inc, err_front_dec = find_errors("Front")
    y_rear_inc, y_rear_dec, err_rear_inc, err_rear_dec = find_errors("Rear")

    plt.subplot(2,2,1)
    plot_subplot(x_front,y_front_inc,err_front_inc,'Front Deadband for Increasing Speed')

    plt.subplot(2,2,2)
    plot_subplot(x_front,y_front_dec,err_front_dec,'Front Deadband for Decreasing Speed')

    plt.subplot(2,2,3)
    plot_subplot(x_rear,y_rear_inc,err_rear_inc,'Rear Deadband for Increasing Speed')

    plt.subplot(2,2,4)
    plot_subplot(x_rear,y_rear_dec,err_rear_dec,'Rear Deadband for Decreasing Speed')

    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    plot_errors()