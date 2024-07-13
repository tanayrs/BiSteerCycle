from matplotlib import pyplot as plt
import numpy as np

front_10_inputs = [130,-140,130,-130]
FRONT_10_START = [input for input in front_10_inputs if input < 0]
FRONT_10_END = [input for input in front_10_inputs if input > 0]

rear_10_inputs = [110,-120,120,-120]
REAR_10_START = [input for input in rear_10_inputs if input < 0]
REAR_10_END = [input for input in rear_10_inputs if input > 0]

front_20_inputs = [130,-110,110,-110]
FRONT_20_START = [input for input in front_20_inputs if input < 0]
FRONT_20_END = [input for input in front_20_inputs if input > 0]

rear_20_inputs = [100,-100,100,-100]
REAR_20_START = [input for input in rear_20_inputs if input < 0]
REAR_20_END = [input for input in rear_20_inputs if input > 0]

front_40_inputs = [70,-90,70,-90]
FRONT_40_START = [input for input in front_40_inputs if input < 0]
FRONT_40_END = [input for input in front_40_inputs if input > 0]

rear_40_inputs = [120,-80,80,-80]
REAR_40_START = [input for input in rear_40_inputs if input < 0]
REAR_40_END = [input for input in rear_40_inputs if input > 0]

x = [10, 10, 20, 20, 40, 40]   # X axis of the graph 

# Front and rear start and end deadbands on the Y axis
front_start = FRONT_10_START + FRONT_20_START + FRONT_40_START
front_end = FRONT_10_END + FRONT_20_END + FRONT_40_END
rear_start = REAR_10_START + REAR_20_START + REAR_40_START
rear_end = REAR_10_END + REAR_20_END + REAR_40_END


# Plotting deadbands on the same graph 
plt.scatter(x, front_start, marker='x', alpha=0.75)
plt.scatter(x, front_end, marker='^', alpha=0.75)
plt.scatter(x, rear_start,marker='p', alpha=0.75)
plt.scatter(x, rear_end,marker='h', alpha=0.75)
# plt.hlines(y=FRONT_10_END, xmin=5, xmax=10,color='k', linestyle='--', linewidth=0.5)
# plt.hlines(y=FRONT_10_START, xmin=5, xmax=10, color='k', linestyle='--', linewidth=0.5)
# plt.hlines(y=FRONT_20_END, xmin=5, xmax=20, color='k', linestyle='--', linewidth=0.5)
# plt.hlines(y=FRONT_20_START, xmin=5, xmax=20, color='k', linestyle='--', linewidth=0.5)
# plt.hlines(y=FRONT_40_END, xmin=5, xmax=40, color='k', linestyle='--', linewidth=0.5)
# plt.hlines(y=FRONT_40_START, xmin=5, xmax=40, color='k', linestyle='--', linewidth=0.5)
# plt.hlines(y=REAR_10_END, xmin=5, xmax=10,color='k', linestyle='--', linewidth=0.5)
# plt.hlines(y=REAR_10_START, xmin=5, xmax=10,color='k', linestyle='--', linewidth=0.5)
# plt.hlines(y=REAR_20_END, xmin=5, xmax=20,color='k', linestyle='--', linewidth=0.5)
# plt.hlines(y=REAR_20_START, xmin=5, xmax=20,color='k', linestyle='--', linewidth=0.5)
# plt.hlines(y=REAR_40_END, xmin=5, xmax=40,color='k', linestyle='--', linewidth=0.5)
# plt.hlines(y=REAR_40_START, xmin=5, xmax=40,color='k', linestyle='--', linewidth=0.5)
# plt.axvline(x=10, color='k', linestyle='--', linewidth=0.5)
# plt.axvline(x=20, color='k', linestyle='--', linewidth=0.5)
# plt.axvline(x=40, color='k', linestyle='--', linewidth=0.5)
# plt.plot(10,FRONT_10_START, 'o')
# plt.plot(10,FRONT_10_END, 'o')
# plt.plot(10,REAR_10_START, 'o')
# plt.plot(10,REAR_10_END, 'o')
# plt.plot(20,FRONT_20_START, 'o')
# plt.plot(20,FRONT_20_END, 'o')
# plt.plot(20,REAR_20_START, 'o')
# plt.plot(20,REAR_20_END, 'o')
# plt.plot(40,FRONT_40_START, 'o')
# plt.plot(40,FRONT_40_END, 'o')
# plt.plot(40,REAR_40_START, 'o')
# plt.plot(40,REAR_40_END, 'o')
# plt.yticks([FRONT_10_START, REAR_10_START, FRONT_20_START, REAR_20_START, FRONT_40_START, REAR_40_START, -50, -25, 0, 25, 50, FRONT_40_END, REAR_40_END, REAR_20_END, FRONT_20_END, REAR_10_START, FRONT_10_END])
plt.xlabel('Slope of Input Speed (PWM per 100ms)',fontsize=14)
plt.ylabel('Deadband Value (PWM)',fontsize=14)
plt.legend(['Front Deadband in -ve Direction', 'Front Deadband +ve Direction', 'Rear Deadband in -ve Direction', 'Rear Deadband in +ve Direction'])
plt.title('Deadband Entry Input Value for Triangle Input of Different Time Periods', fontsize=14)
plt.grid()
plt.show()