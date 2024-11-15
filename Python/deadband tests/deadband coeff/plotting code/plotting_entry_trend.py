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

# plotting kinetic coefficients with speed (front and rear, increasing and decreasing)
def plot_trend_avg(df_front, df_rear):
    # Speed to be plotted on x axis 
    speeds_front = list(df_front['speed'])
    speeds_rear = list(df_rear['speed']) 

    # Kinetic coefficients for increasing speed
    coeffs_inc_front = list(df_front['kinetic_coeff_inc'])
    coeffs_inc_rear = list(df_rear['kinetic_coeff_inc'])

    # Kinetic coefficients for increasing speed
    coeffs_dec_front = list(df_front['kinetic_coeff_dec'])
    coeffs_dec_rear = list(df_rear['kinetic_coeff_dec'])

    plt.figure(figsize=(14,8.5))
    plt.plot(speeds_front, coeffs_dec_front)
    plt.plot(speeds_front, coeffs_inc_front)
    plt.plot(speeds_rear, coeffs_dec_rear)
    plt.plot(speeds_rear, coeffs_inc_rear)

    plt.scatter(speeds_front, coeffs_dec_front)
    plt.scatter(speeds_front, coeffs_inc_front)
    plt.scatter(speeds_rear, coeffs_dec_rear)
    plt.scatter(speeds_rear, coeffs_inc_rear)

    # plt.axhline(max(coeffs_dec_front), color='k', linestyle='--', linewidth=1)
    # plt.axhline(max(coeffs_inc_front), color='k', linestyle='--', linewidth=1)
    # plt.axhline(min(coeffs_dec_front), color='k', linestyle='--', linewidth=1)
    # plt.axhline(min(coeffs_inc_front), color='k', linestyle='--', linewidth=1)

    # plt.axhline(max(coeffs_dec_rear), color='k', linestyle='--', linewidth=1)
    # plt.axhline(max(coeffs_inc_rear), color='k', linestyle='--', linewidth=1)
    # plt.axhline(min(coeffs_dec_rear), color='k', linestyle='--', linewidth=1)
    # plt.axhline(min(coeffs_inc_rear), color='k', linestyle='--', linewidth=1)

    plt.xlabel('Slope of Input Speed (PWM per 100ms)',fontsize=14)
    plt.ylabel('Deadband Value (PWM)',fontsize=14)
    plt.legend(['Front Deadband for Decreasing Speed', 'Front Deadband for Increasing Speed', 'Rear Deadband for Decreasing Speed', 'Rear Deadband for Increasing Speed'], loc='center right', fontsize=14)
    plt.title('Deadband Entry for Different Slopes of Input Triangle Wave', fontsize=14)
    plt.xticks([1,2,3,4,5,6,7,8,9,10,15,20,25,30,35])
    plt.yticks(range(-175,176,25))
    plt.grid()
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    plt.show()

def plot_kinetic_avg():
    PLOTTING_CONSTANTS_PATH = './Python/deadband tests/deadband coeff/plot constants/plotting_constants.csv'
    df = pd.read_csv(PLOTTING_CONSTANTS_PATH)

    df_front = df.where(df['motor'] == 'front')
    df_rear = df.where(df['motor'] == 'rear')
    df_front.dropna(inplace=True)
    df_rear.dropna(inplace=True)

    print(df_front[['kinetic_coeff_inc', 'kinetic_coeff_dec']].describe())
    print(df_rear[['kinetic_coeff_inc', 'kinetic_coeff_dec']].describe())

    plot_trend_avg(df_front, df_rear)

def find_errors(motor):
    y_inc = []
    y_dec = []
    y_min = []
    y_max = []
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
        y_min.append(df['kinetic_coeffs_inc'].min())
        y_max.append(df['kinetic_coeffs_dec'].max())
        err_inc.append(abs(df['kinetic_coeffs_inc'].std()))
        err_dec.append(abs(df['kinetic_coeffs_dec'].std()))

    return (y_inc, y_dec, y_min, y_max, err_inc, err_dec)

def plot_subplot(x, y, ylim, err, label):
    plt.errorbar(x, y, err, label=label, capsize=5)
    plt.scatter(x, y)
    plt.xlabel('Slope of Input Speed (PWM per 100ms)',fontsize=14)
    plt.ylabel('Deadband Value (PWM)',fontsize=14)
    plt.xticks([1,2,3,4,5,6,7,8,9,10,15,20,25,30,35])
    if max(ylim) > 0:
        plt.ylim([0, max(ylim)])
    else:
        plt.ylim([min(ylim),0])
    plt.grid()
    plt.title(label,fontsize=18)
    
def plot_errors():
    y_front_inc, y_front_dec, y_min_front, y_max_front, err_front_inc, err_front_dec = find_errors("Front")
    y_rear_inc, y_rear_dec, y_min_rear, y_max_rear, err_rear_inc, err_rear_dec = find_errors("Rear")

    plt.subplot(2,2,1)
    plot_subplot(x_front,y_front_inc,y_min_front,err_front_inc,'Front Deadband for Increasing Speed')

    plt.subplot(2,2,2)
    plot_subplot(x_front,y_front_dec,y_max_front,err_front_dec,'Front Deadband for Decreasing Speed')

    plt.subplot(2,2,3)
    plot_subplot(x_rear,y_rear_inc,y_min_rear,err_rear_inc,'Rear Deadband for Increasing Speed')

    plt.subplot(2,2,4)
    plot_subplot(x_rear,y_rear_dec,y_max_rear,err_rear_dec,'Rear Deadband for Decreasing Speed')

    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # plot_trend_avg
    plot_errors()