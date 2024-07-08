from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

PLOTTING_CONSTANTS_PATH = './Python/deadband coeff/plotting_constants.csv'
df = pd.read_csv(PLOTTING_CONSTANTS_PATH)

df_front = df.where(df['motor'] == 'front')
df_rear = df.where(df['motor'] == 'rear')
df_front.dropna(inplace=True)
df_rear.dropna(inplace=True)

print(df_front[['static_coeff_inc', 'static_coeff_dec']].describe())
print(df_rear[['static_coeff_inc', 'static_coeff_dec']].describe())


# Speed to be plotted on x axis 
speeds_front = list(df_front['speed'])
speeds_rear = list(df_rear['speed']) 

# static  coefficients for increasing speed
coeffs_inc_front = list(df_front['static_coeff_inc'])
coeffs_inc_rear = list(df_rear['static_coeff_inc'])

# static  coefficients for increasing speed
coeffs_dec_front = list(df_front['static_coeff_dec'])
coeffs_dec_rear = list(df_rear['static_coeff_dec'])

# plotting static  coefficients with speed (front and rear, increasing and decreasing)
plt.plot(speeds_front, coeffs_dec_front)
plt.plot(speeds_front, coeffs_inc_front)
plt.plot(speeds_rear, coeffs_dec_rear)
plt.plot(speeds_rear, coeffs_inc_rear)

plt.scatter(speeds_front, coeffs_dec_front)
plt.scatter(speeds_front, coeffs_inc_front)
plt.scatter(speeds_rear, coeffs_dec_rear)
plt.scatter(speeds_rear, coeffs_inc_rear)

plt.xlabel('Slope of Input Speed (PWM per 100ms)',fontsize=14)
plt.ylabel('Deadband Value (PWM)',fontsize=14)
plt.legend(['Front Deadband decreasing', 'Front Deadband increasing', 'Rear Deadband decreasing', 'Rear Deadband in increasing'])
plt.xticks([1,2,3,4,5,6,7,8,9,10,15,20,25,30,35])
plt.yticks(range(-225,226,25))
plt.title('Deadband Exit for Different Slopes of Input Triangle Wave', fontsize=14)
manager = plt.get_current_fig_manager()
manager.full_screen_toggle()
plt.show()