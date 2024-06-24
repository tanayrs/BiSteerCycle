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

x = [10, 20, 40]   # X axis if the graph 

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
plt.xlabel('Slope of Input Speed (PWM/ms)')
plt.ylabel('Deadband value')
plt.legend(['Front deadband start', 'Front deadband end', 'Rear deadband start', 'Rear deadband end'])
plt.show()