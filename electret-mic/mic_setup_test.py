import analogio
import time

# Configure the ADC pin for the MAX4466
mic = analogio.AnalogIn(board.A0)

while True:
    mic_value = mic.value  # Read the raw ADC value (0-65535)
    print(mic_value)       # Output the value to the serial console
    time.sleep(0.01)       # Short delay to avoid flooding


