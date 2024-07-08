'''
Experiment: Plotting static deadband coefficients for different slopes with error bars
By: Jia Bhargava, Tanay Srinivasa
Last Modified: 3 Jul 2024
'''

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

x_front = [2,3,4,5,6,7,8,9,10,15,20,25,30]
x_rear = [2,4,5,6,7,8,9,10,15,40]
x = [1,2,3,4,5,6,7,8,9,10,15,20,25,30,35,40] 
x_front = x
x_rear = x

def find_errors(motor):
    y_inc = []
    y_dec = []
    err_inc = []
    err_dec = []

    # if motor == "Front":
    #     x = x_front
    # else:
    #     x = x_rear

    for i in x:
        path = f'./Python/deadband tests/deadband coeff/plot constants/CombinedConstants/{motor}Slope{i}Constants.csv'
        df = pd.read_csv(path)
        y_inc.append(df['static_coeffs_inc'].mean())
        y_dec.append(df['static_coeffs_dec'].mean())
        err_inc.append(abs(df['static_coeffs_inc'].std()))
        err_dec.append(abs(df['static_coeffs_dec'].std()))

    return (y_inc, y_dec, err_inc, err_dec)

y_front_inc, y_front_dec, err_front_inc, err_front_dec = find_errors("Front")
y_rear_inc, y_rear_dec, err_rear_inc, err_rear_dec = find_errors("Rear")


plt.errorbar(x_front, y_front_inc, err_front_inc, label='Front Deadband for Increasing Speed', capsize=5)
plt.errorbar(x_front, y_front_dec, err_front_dec, label='Front Deadband for Decreasing Speed', capsize=5)
plt.errorbar(x_rear, y_rear_inc, err_rear_inc, label='Rear Deadband for Increasing Speed', capsize=5)
plt.errorbar(x_rear, y_rear_dec, err_rear_dec, label='Rear Deadband for Decreasing Speed', capsize=5)

plt.scatter(x_front, y_front_inc)
plt.scatter(x_front, y_front_dec)
plt.scatter(x_rear, y_rear_inc)
plt.scatter(x_rear, y_rear_dec)


plt.xlabel('Slope of Input Speed (PWM per 100ms)',fontsize=14)
plt.ylabel('Deadband Value (PWM)',fontsize=14)
plt.legend(loc='center right', fontsize=14)
plt.title('Deadband Exit for Different Slopes of Input Triangle Wave with error bars', fontsize=14)
plt.xticks([1,2,3,4,5,6,7,8,9,10,15,20,25,30,35])
plt.yticks(range(-200,201,50))
plt.grid()
manager = plt.get_current_fig_manager()
manager.full_screen_toggle()
plt.show()