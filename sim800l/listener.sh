#!/bin/bash

# Load the target email from the environment variable
target_email=$(printenv target_email)

# Set up logging
log_file="/var/log/rpi_camera.log"

# Set up signal trap to capture SIGUSR1 and take a picture
trap 'take_picture' SIGUSR1

# Function to take a picture and send it via email
take_picture() {
    # Take a picture with the Raspberry Pi camera
    image_file="/tmp/$(date +'%Y-%m-%d-%H-%M-%S').jpg"
    raspistill -o "$image_file"

    # Check if the image was taken successfully
    if [ $? -ne 0 ]; then
        echo "$(date) - Error taking picture" >> "$log_file"
        return 1
    fi

    # Send the image via email
    echo "$(date) - Sending picture to $target_email" >> "$log_file"
    echo "Picture taken at $(date)" | mail -s "Raspberry Pi Picture" -A "$image_file" "$target_email"

    # Check if the email was sent successfully
    if [ $? -ne 0 ]; then
        echo "$(date) - Error sending email" >> "$log_file"
        return 1
    fi

    # Remove the image file
    rm "$image_file"
}

# Run indefinitely and wait for signals
while true; do
    sleep 1
done
