from matplotlib import pyplot as plt
import numpy as np


FRONT_10_START = -135
FRONT_10_END = 130

REAR_10_START = -120
REAR_10_END = 115

FRONT_20_START = -110
FRONT_20_END = 120

REAR_20_START = -100
REAR_20_END = 100

FRONT_40_START = -90
FRONT_40_END = 70

REAR_40_START = -80
REAR_40_END = 90

x = [10, 20, 40]   # X axis of the graph 

# Front and rear start and end deadbands on the Y axis
front_start = [FRONT_10_START, FRONT_20_START, FRONT_40_START]
front_end = [FRONT_10_END, FRONT_20_END, FRONT_40_END]
rear_start = [REAR_10_START, REAR_20_START, REAR_40_START] 
rear_end = [REAR_10_END, REAR_20_END, REAR_40_END]


# Plotting deadbands on the same graph 
plt.plot(x, front_start)
plt.plot(x, front_end)
plt.plot(x, rear_start)
plt.plot(x, rear_end)
plt.hlines(y=FRONT_10_END, xmin=5, xmax=10,color='k', linestyle='--', linewidth=0.5)
plt.hlines(y=FRONT_10_START, xmin=5, xmax=10, color='k', linestyle='--', linewidth=0.5)
plt.hlines(y=FRONT_20_END, xmin=5, xmax=20, color='k', linestyle='--', linewidth=0.5)
plt.hlines(y=FRONT_20_START, xmin=5, xmax=20, color='k', linestyle='--', linewidth=0.5)
plt.hlines(y=FRONT_40_END, xmin=5, xmax=40, color='k', linestyle='--', linewidth=0.5)
plt.hlines(y=FRONT_40_START, xmin=5, xmax=40, color='k', linestyle='--', linewidth=0.5)
plt.hlines(y=REAR_10_END, xmin=5, xmax=10,color='k', linestyle='--', linewidth=0.5)
plt.hlines(y=REAR_10_START, xmin=5, xmax=10,color='k', linestyle='--', linewidth=0.5)
plt.hlines(y=REAR_20_END, xmin=5, xmax=20,color='k', linestyle='--', linewidth=0.5)
plt.hlines(y=REAR_20_START, xmin=5, xmax=20,color='k', linestyle='--', linewidth=0.5)
plt.hlines(y=REAR_40_END, xmin=5, xmax=40,color='k', linestyle='--', linewidth=0.5)
plt.hlines(y=REAR_40_START, xmin=5, xmax=40,color='k', linestyle='--', linewidth=0.5)
plt.axvline(x=10, color='k', linestyle='--', linewidth=0.5)
plt.axvline(x=20, color='k', linestyle='--', linewidth=0.5)
plt.axvline(x=40, color='k', linestyle='--', linewidth=0.5)
plt.plot(10,FRONT_10_START, 'o')
plt.plot(10,FRONT_10_END, 'o')
plt.plot(10,REAR_10_START, 'o')
plt.plot(10,REAR_10_END, 'o')
plt.plot(20,FRONT_20_START, 'o')
plt.plot(20,FRONT_20_END, 'o')
plt.plot(20,REAR_20_START, 'o')
plt.plot(20,REAR_20_END, 'o')
plt.plot(40,FRONT_40_START, 'o')
plt.plot(40,FRONT_40_END, 'o')
plt.plot(40,REAR_40_START, 'o')
plt.plot(40,REAR_40_END, 'o')
plt.yticks([FRONT_10_START, REAR_10_START, FRONT_20_START, REAR_20_START, FRONT_40_START, REAR_40_START, -50, -25, 0, 25, 50, FRONT_40_END, REAR_40_END, REAR_20_END, FRONT_20_END, REAR_10_START, FRONT_10_END])
plt.xlabel('Slope of Input Speed (PWM per 100ms)',fontsize=14)
plt.ylabel('Deadband Value (PWM)',fontsize=14)
plt.legend(['Front Deadband in -ve Direction', 'Front Deadband +ve Direction', 'Rear Deadband in -ve Direction', 'Rear Deadband in +ve Direction'])
plt.title('Deadband Entry Input Value for Triangle Input of Different Time Periods', fontsize=14)
plt.show()