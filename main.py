import matplotlib  # Import matplotlib library for plotting
matplotlib.use('TkAgg')  # Force TkAgg backend for interactive plotting windows (required for live animations)
import serial  # Import pyserial library to communicate with Arduino via USB
import time  # Import time library to handle delays and timestamps
from collections import deque  # Import deque for efficient fixed-size list (auto-removes oldest data)
import matplotlib.pyplot as plt  # Import pyplot for creating plots and graphs
from matplotlib.animation import FuncAnimation  # Import FuncAnimation to create live updating animations

SERIAL_PORT = '/dev/cu.usbmodem11201'  # Define the USB port where Arduino is connected (Mac format)
BAUD_RATE = 9600  # Set communication speed to 9600 bits per second (must match Arduino code)
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)  # Create serial connection object with 1 second timeout
time.sleep(2)  # Wait 2 seconds for Arduino to reset and stabilize after connection
ser.reset_input_buffer()  # Clear any old/garbage data from the serial buffer
print("Connected to Arduino. Waiting for data...")  # Inform user that connection is established
print("We are starting the graph now. It will open in a different window.")  # Notify user about separate window

times = deque(maxlen=100)  # Create deque to store last 100 time values (x-axis data)
temperatures = deque(maxlen=100)  # Create deque to store last 100 temperature readings
humidities = deque(maxlen=100)  # Create deque to store last 100 humidity readings

start_time = time.time()  # Record the program start time as reference point for elapsed time
print(start_time)  # Print the start timestamp (for debugging purposes)

def animate(i):  # Define animation function that runs repeatedly (i = frame number)
    try:  # Start error handling block to catch any exceptions

        if ser.in_waiting > 0:  # Check if data is available in the serial buffer
            line = ser.readline().decode('utf-8').strip()  # Read one line, convert bytes to string, remove whitespace
            if line:  # If line is not empty
                print(f"Received: {line}")  # Print received data to console for debugging

            if line and line != "ERROR":  # If line exists and is not an error message from Arduino
                # Parse temperature and humidity
                values = line.split(',')  # Split the CSV string by comma into a list
                if len(values) == 2:  # Check if exactly 2 values exist (temp and humid)
                    try:  # Start error handling for data conversion
                        temp = float(values[0])  # Convert first value (temperature) to float
                        humid = float(values[1])  # Convert second value (humidity) to float

                        # Append data
                        current_time = time.time() - start_time  # Calculate elapsed time since start
                        times.append(current_time)  # Add current time to deque (oldest auto-removed if > 100)
                        temperatures.append(temp)  # Add temperature to deque
                        humidities.append(humid)  # Add humidity to deque

                    except ValueError:  # If conversion to float fails
                        print(f"Invalid data format: {line}")  # Print error message with bad data

    except Exception as e:  # Catch any other unexpected errors
        print(f"Error: {e}")  # Print the error message

    plt.cla()  # Clear the current plot axes (erases previous frame)

    if len(times)>0:  # Check if there's data to plot (prevents error on empty deques)
        plt.plot(times, temperatures, label='Temperature')  # Plot temperature line (x=times, y=temperatures)
        plt.plot(times, humidities, label='Humidity')  # Plot humidity line (x=times, y=humidities)
    plt.xlabel('Time')  # Set x-axis label to 'Time'
    plt.ylabel('Temp and Humidity')  # Set y-axis label to 'Temp and Humidity'
    plt.title('Temperature and Humidity Monitoring')  # Set graph title
    plt.legend(loc='upper right')  # Add legend in upper right corner showing which line is which

ani = FuncAnimation(plt.gcf(),  # Create animation object using current figure (gcf = get current figure)
                    animate,  # Specify the function to call repeatedly
                    interval=1000,  # Call animate function every 1000 milliseconds (1 second)
                    cache_frame_data=False)  # Don't cache frame data (saves memory, removes warning)

plt.tight_layout()  # Adjust plot spacing to prevent label cutoff

try:  # Start error handling block
    plt.show()  # Display the plot window and start the animation loop (blocking call)
except KeyboardInterrupt:  # If user presses Ctrl+C
    print("\nStopping...")  # Print stopping message
finally:  # Always execute this block, even if error occurs
    ser.close()  # Close the serial connection to free the port