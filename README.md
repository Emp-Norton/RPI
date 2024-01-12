![2024-01-11-214446_1024x768_scrot](https://github.com/Emp-Norton/RPI/assets/20247410/7a3a4a7b-a6f6-4b76-a387-5fa4db68f02a)
# RPI
A personal repo for goofing around with RPi accessories and such.

## Lights [TODO: this]

## Lidar 
### Parking by sight instead of sound
This is a small project I created to help park my truck in SF, especially at night, as well as to familiarize myself with lidar technology and get some practice creating GUIs in python rather than the standard web development I've mostly been up to. 

In this project, I'm leveraging the very affordable TF_Luna lidar module and a raspberry pi camera aligned and mounted in a housing, then attached to the inside of my truck's grill. This allows me to create a realtime display of what is immediately in front of the massive front end of the vehicle that's usually obscured, as well as get an accurate (up to 8 meters) distance reading--how long before things start to crunch. I've found a small adapter that allows me to use HDMI instead of CSI cables which dramatically improved picture quality, reduced interference and latency, and is generally far more durable and robust than ribbon cables. More to come. 

There are a few example images in the repo, demonstrating  the display, the effective targetting reticule, the warning that's created when the objects sensed inside the target are less than 1 meter away, etc.
