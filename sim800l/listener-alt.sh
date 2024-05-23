#!/bin/bash

# Load the target email from the environment variable
target_email=$(printenv target_email)

# Set up logging
log_file="/var/log/rpi_camera.log"

# Set up signal trap to take picture and send email when signal is received
trap take_picture_and_send_email SIGUSR1

# Function to take picture and send email
take_picture_and_send_email() {
    # Take a picture with the raspberry pi camera
    picture_path="/tmp/picture.jpg"
    raspistill -o "$picture_path"

    # Check if the picture was taken successfully
    if [ $? -ne 0 ]; then
        echo "Failed to take picture" >> "$log_file"
        return 1
    fi

    # Send the picture via email using mpack
    mpack -s "Raspberry Pi Picture" "$picture_path" "$target_email"

    # Check if the email was sent successfully
    if [ $? -ne 0 ]; then
        echo "Failed to send email" >> "$log_file"
        return 1
    fi

    # Log success
    echo "Picture taken and sent to $target_email successfully" >> "$log_file"
}

# Run indefinitely and wait for signals
while true; do
    sleep 1
done

