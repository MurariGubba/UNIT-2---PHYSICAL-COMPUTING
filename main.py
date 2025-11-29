import matplotlib

import serial
import time
from itertools import count
import pandas as pd
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

SERIAL_PORT = '/dev/cu.usbmodem11401'
BAUD_RATE = 9600
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Wait for connection to establish
ser.reset_input_buffer()
print("Connected to Arduino. Waiting for data...")

max_points = 100
times = deque(maxlen=max_points)
temperatures = deque(maxlen=max_points)
humidities = deque(maxlen=max_points)

index = count()
start_time = time.time()

def animate(i):
    try:

        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if line:
                print(f"Received: {line}")  # Debug print

            if line and line != "ERROR":
                # Parse temperature and humidity
                values = line.split(',')
                if len(values) == 2:
                    try:
                        temp = float(values[0])
                        humid = float(values[1])

                        # Append data
                        current_time = time.time() - start_time
                        times.append(current_time)
                        temperatures.append(temp)
                        humidities.append(humid)

                    except ValueError:
                        print(f"Invalid data format: {line}")

    except Exception as e:
        print(f"Error: {e}")
