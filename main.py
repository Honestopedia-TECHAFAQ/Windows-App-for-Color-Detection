import pygetwindow as gw
import pyautogui
import numpy as np
import tkinter as tk
import time
import threading
import subprocess  # For running a custom script
import sys
import winsound  # For playing a beep sound on Windows

# Define multiple target colors (e.g., red, green, blue)
TARGET_COLORS = [
    (255, 0, 0),  # Red
    (0, 255, 0),  # Green
    (0, 0, 255),  # Blue
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
]
COLOR_TOLERANCE = 50  # Tolerance level for color matching

# Function to detect the target colors within a specific window
def detect_color_in_window(window_title):
    try:
        # Find the window by title
        window = gw.getWindowsWithTitle(window_title)
        if window:
            win = window[0]
            # Bring window to the front if minimized or not focused
            if not win.isActive:
                win.activate()
            # Get the window's region (x, y, width, height)
            region = (win.left, win.top, win.width, win.height)
            # Take a screenshot of the window region
            screenshot = pyautogui.screenshot(region=region)
            img_array = np.array(screenshot)
            print(f"Screenshot captured from region: {region}")
            print(f"Screenshot size: {img_array.shape}")  # Print the size of the screenshot

            # Convert to RGB format (just in case it's RGBA)
            img_array = img_array[:, :, :3]
            
            # Print a sample pixel to check if the data looks correct
            print(f"Sample pixel: {img_array[0, 0]}")  # Print the top-left corner pixel for debugging
            
            # Check if target color exists in the image
            for target_color in TARGET_COLORS:
                if np.any(np.all(np.abs(img_array - target_color) <= COLOR_TOLERANCE, axis=-1)):
                    print(f"Target color {target_color} detected!")
                    return True
            return False
        else:
            print("Window not found.")
        return False
    except Exception as e:
        print(f"Error detecting color: {e}")
        return False

# Function to execute the custom Python script when a color is detected
def execute_script(detected_color):
    print(f"Target color {detected_color} detected! Executing the script...")
    # Example: Trigger another Python script
    try:
        subprocess.run([sys.executable, "your_script.py"], check=True)  # Replace with your script
        print("Script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running the script: {e}")

# Function to play a beep sound when a color is detected
def play_beep():
    winsound.Beep(1000, 500)  # Frequency of 1000 Hz for 500 ms

# Threaded function to monitor the window in the background
def monitor_window(window_title):
    while monitoring_flag:
        detected_color = detect_color_in_window(window_title)
        if detected_color:
            play_beep()  # Play the beep sound when the color is detected
            update_status(f"Target color {detected_color} detected!", "green")  # Update status with color name
            execute_script(detected_color)
        else:
            update_status("No target colors detected.", "red")  # Update status when no color is found
        time.sleep(1)  # Adjust delay for performance

# Function to update the status label on the UI
def update_status(message, color):
    status_label.config(text=message, bg=color)
    status_label.update_idletasks()

# Start/Stop monitoring function
def toggle_monitoring():
    global monitoring_flag
    if monitoring_flag:
        monitoring_flag = False
        start_button.config(text="Start Monitoring")
        print("Monitoring stopped.")
    else:
        monitoring_flag = True
        start_button.config(text="Stop Monitoring")
        # Start the monitor in a separate thread to avoid blocking the main UI
        threading.Thread(target=monitor_window, args=("Your Window Title Here",), daemon=True).start()
        print("Monitoring started.")

# Create the Tkinter window
root = tk.Tk()
root.title("Window Color Monitor")

# Set up the start/stop button
start_button = tk.Button(root, text="Start Monitoring", command=toggle_monitoring)
start_button.pack(pady=20)

# Label to show the detection status
status_label = tk.Label(root, text="No target colors detected.", width=40, height=2)
status_label.pack(pady=20)

# Flag to control monitoring
monitoring_flag = False

# Run the Tkinter event loop
root.mainloop()
