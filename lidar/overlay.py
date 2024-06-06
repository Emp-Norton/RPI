#To add an image overlay, you can use the cv2.addWeighted function to overlay the image on the video frame. The background transparency of the overlay image does not matter, as you can adjust the alpha channel when overlaying the image.

#Here's how you can do it:

import cv2, os, sys
import numpy as np
import tkinter as tk

from lidar import get_lidar_distance
from PIL import Image, ImageTk

filename = 'image.png'
overlay_path = '/home/pi/projects/RPI/lidar/' + filename

def draw_target_mark(img, panel):
    origin_x = int(panel.winfo_width() / 2)
    origin_y = int(panel.winfo_height() / 2)
    cir_radius = 70
    cv2.circle(img, (origin_x, origin_y), cir_radius, (0,0,255), 1)

# Function to update GUI with new frame
def update_gui():
    try:
        # Read frame from camera
        _, frame = cap.read()

        # Get distance from TF-Luna Lidar (replace this with your actual implementation)
        try:
            lidar_distance = get_lidar_distance()
        except Exception as e:
             print(f"Failed to load lidar distance. Error: {e}")
        warning_text = f"WARNING! {lidar_distance} m! Too close!"
        overlay_text = None
        color_tuple = (0,255,0)
        # Overlay lidar distance on the frame
        if lidar_distance is not None:
            overlay_text = f"Lidar Distance: {lidar_distance} m"
            if lidar_distance <= 1:
                overlay_text = warning_text
                color_tuple = (0,0,255)
            cv2.putText(frame, overlay_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color_tuple, 2)

        # Load the overlay image
        overlay = cv2.imread(overlay_path, cv2.IMREAD_UNCHANGED)

        # Resize the overlay to match the frame size
        overlay = cv2.resize(overlay, (frame.shape[1], frame.shape[0]))

        # Overlay the image on the frame
        alpha = 0.5  # adjust the alpha channel to change the overlay transparency
        frame = cv2.addWeighted(frame, 1, overlay[:, :, 0:3], alpha, 0)

        # Convert frame to RGB format for tkinter
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert to ImageTk format
        draw_target_mark(frame_rgb, panel)
        img = Image.fromarray(frame_rgb)
        img_tk = ImageTk.PhotoImage(image=img)

        # Update the label in the GUI
        panel.img_tk = img_tk
        panel.config(image=img_tk)
        panel.after(10, update_gui)  # Schedule the next update
    except KeyboardInterrupt:
        print("User sent interrupt. Quitting.")
        sys.exit()

try:
    # Set up camera
    cap = cv2.VideoCapture(0)

    # Set up GUI
    root = tk.Tk()
    root.title("Camera and Lidar Overlay")

    # Create a label for displaying the video feed
    panel = tk.Label(root)
    panel.pack(padx=10, pady=10)

    # Call the update function to start the GUI
    update_gui()

    # Start the Tkinter main loop
    root.mainloop()

    # Release resources when the GUI is closed
    cap.release()
    cv2.destroyAllWindows()
except KeyboardInterrupt:
    print("User sent interrupt. Quitting.")
    sys.exit()
