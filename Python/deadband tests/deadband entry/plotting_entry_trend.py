'''
Experiment: Plotting kinetic deadband coefficients for different slopes with error bars
By: Jia Bhargava, Tanay Srinivasa
Last Modified: 3 Jul 2024
'''

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

front_inc = {'10': np.array([-140,-130]),
             '20': np.array([-110,-110]),
             '40': np.array([-90,-90])}

front_dec = {'10': np.array([130,130]),
             '20': np.array([130,110]),
             '40': np.array([70,70])}

rear_inc = {'10': np.array([-120,-120]),
             '20': np.array([-100,-100]),
             '40': np.array([-80,-80])}

rear_dec = {'10': np.array([110,120]),
             '20': np.array([100,100]),
             '40': np.array([120,80])}

x_front = [10,20,40]
x_rear = [10,20,40]

def find_errors(motor):
    y_inc = []
    y_dec = []
    err_inc = []
    err_dec = []

    if motor == "Front":
        for i in x_front:
            y_inc.append(front_inc[str(i)].mean())
            y_dec.append(front_dec[str(i)].mean())
            err_inc.append(abs(front_inc[str(i)].std()))
            err_dec.append(abs(front_inc[str(i)].std()))
    else:
        for i in x_rear:
            y_inc.append(rear_inc[str(i)].mean())
            y_dec.append(rear_dec[str(i)].mean())
            err_inc.append(abs(rear_inc[str(i)].std()))
            err_dec.append(abs(rear_inc[str(i)].std()))

    return (y_inc, y_dec, err_inc, err_dec)

def plot_subplot(x, y, err, label):
    plt.errorbar(x, y, err, label=label, capsize=5)
    plt.scatter(x, y)
    plt.xlabel('Slope of Input Speed (PWM per 100ms)',fontsize=14)
    plt.ylabel('Deadband Value (PWM)',fontsize=14)
    plt.xticks([10,20,40])
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
    # plot_trend_avg
    plot_errors()