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