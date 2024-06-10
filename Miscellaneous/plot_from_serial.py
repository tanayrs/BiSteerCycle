import serial
import time
import csv

with open('SensorData.csv', mode='w') as sensor_file:
    sensor_writer = csv.writer(sensor_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    sensor_writer.writerow(["Time", "Angle"])
    
com = "/dev/cu.usbmodem160464801"
baud = 9600

x = serial.Serial(com, baud, timeout=0.1)

while x.isOpen() is True:
    data = str(x.readline().decode('utf-8')).rstrip()
    if data != '':
        with open('SensorData.csv', mode='a') as sensor_file:
            line = data.split(' ')
            sensor_writer = csv.writer(sensor_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            sensor_writer.writerow([line[0],line[1]])