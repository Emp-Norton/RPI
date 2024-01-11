import cv2, sys
import numpy as np
import tkinter as tk

from lidar import get_lidar_distance
from PIL import Image, ImageTk

def draw_target_mark(img, panel):
    origin_x = int(panel.winfo_width() / 2)
    origin_y = int(panel.winfo_height() / 2)
    cv2.circle(img, (origin_x, origin_y), 30, (0,0,255), 1)

# Function to update GUI with new frame
def update_gui():
    try:
        # Read frame from camera
        _, frame = cap.read()

        # Get distance from TF-Luna Lidar (replace this with your actual implementation)
        lidar_distance = get_lidar_distance()
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

