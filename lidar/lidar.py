import serial
import time

# Serial port configuration
ser = serial.Serial('/dev/serial0', baudrate=115200, timeout=1)

# Function to get Lidar distance

def get_lidar_distance():
    try:
        # Send command to TF-Luna
        ser.write(b'\x42\x57\x02\x00\x00\x00\x01\x06')

        # Read and parse response
        response = ser.read(9)
        if len(response) == 9 and response[0] == 0x59 and response[1] == 0x59:
            distance = (response[2] + response[3] * 256) / 100.0
            return distance
        else:
            print("Invalid response from TF-Luna")
    except Exception as e:
        print(f"Error: {e}")

    return None

# Wait for Lidar to initialize
time.sleep(2)


#while True:
#   lidar_distance = get_lidar_distance()
#    if lidar_distance is not None:
#        print(f"Lidar Distance: {lidar_distance} cm")
#    time.sleep(0.1)  # Adjust the delay as needed
