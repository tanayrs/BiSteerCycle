'''
Experiment: Finding Trend of Deadband Entry and Exit PWM Values with Varying Acceleration
By: Jia Bhargava, Tanay Srinivasa
Last Modified: 1 Jul 2024

Run bi_steer_cycle_testing arduino code with deadband_test()
'''
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

PLOTTING_CONSTANTS_PATH = './Python/deadband tests/deadband coeff/plot constants/plotting_constants.csv'
df = pd.read_csv(PLOTTING_CONSTANTS_PATH)

df_front = df.where(df['motor'] == 'front')
df_rear = df.where(df['motor'] == 'rear')
df_front.dropna(inplace=True)
df_rear.dropna(inplace=True)

print(df_front[['kinetic_coeff_inc', 'kinetic_coeff_dec']].describe())
print(df_rear[['kinetic_coeff_inc', 'kinetic_coeff_dec']].describe())


# Speed to be plotted on x axis 
speeds_front = list(df_front['speed'])
speeds_rear = list(df_rear['speed']) 

# Kinetic coefficients for increasing speed
coeffs_inc_front = list(df_front['kinetic_coeff_inc'])
coeffs_inc_rear = list(df_rear['kinetic_coeff_inc'])

# Kinetic coefficients for increasing speed
coeffs_dec_front = list(df_front['kinetic_coeff_dec'])
coeffs_dec_rear = list(df_rear['kinetic_coeff_dec'])

# plotting kinetic coefficients with speed (front and rear, increasing and decreasing)
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