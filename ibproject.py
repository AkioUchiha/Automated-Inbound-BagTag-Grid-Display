import time
import tkinter as tk
from tkinter import Label
import pytesseract
import pyautogui
import threading
from pynput import mouse
import re
import csv

pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\akio.apollobishwal\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'

# Variables to store the coordinates
click_count = 0
top_left = None
bottom_right = None

# Function to display coordinates on the screen
def display_coordinates(top_left, bottom_right):
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.geometry(f"{bottom_right[0] - top_left[0]}x{bottom_right[1] - top_left[1]}+{top_left[0]}+{top_left[1]}")

    canvas = tk.Canvas(root, bg='black')
    canvas.pack(fill=tk.BOTH, expand=tk.YES)

    # Draw the rectangle box
    canvas.create_rectangle(0, 0, bottom_right[0] - top_left[0], bottom_right[1] - top_left[1], outline='white', width=2)

    root.after(5000, root.destroy)  # Close after 5 seconds
    root.mainloop()


def on_click(x, y, button, pressed):
    global click_count, top_left, bottom_right
    if pressed:
        click_count += 1
        if click_count == 2:
            top_left = (x, y)
            print(f"Top-left corner: {top_left}")
            print("Move your mouse to the desired bottom-right corner and click.")
        elif click_count == 3:
            bottom_right = (x, y)
            print(f"Bottom-right corner: {bottom_right}")
            display_coordinates(top_left, bottom_right)
            return False  # Stop the listener

print("Move your mouse to the desired top-left corner of the region and click.")
print("Then, move your mouse to the desired bottom-right corner and click.")
with mouse.Listener(on_click=on_click) as listener:
    listener.join()

region = (top_left[0], top_left[1], bottom_right[0] - top_left[0], bottom_right[1] - top_left[1])
print(f"Region: {region}")

# Load target texts and corresponding letters from CSV file
def load_target_texts(csv_filename):
    target_texts = {}
    with open(csv_filename, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if len(row) < 2:
                continue  # Skip rows that do not have at least two columns
            target_texts[row[0]] = row[1]
    return target_texts

# Initialize the Tkinter window and label
root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
root.configure(bg='black')

# Create the label with initial settings
label = Label(root, text="", font=('Helvetica', 128), fg='white', bg='black')
label.pack()

# Update the geometry to fit the label's size
root.update_idletasks()
window_width = label.winfo_reqwidth()
window_height = label.winfo_reqheight()

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate position to center horizontally and near the top
x = (screen_width // 2) - (window_width // 2)
y = screen_height // 5  # Adjust this value to move the window up/down

# Set the window position and size
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Function to show the overlay
def show_overlay(letter):
    # Update the label text and color to yellow
    label.config(text=letter, fg='yellow')

    # Update the geometry to fit the new label size
    root.update_idletasks()
    window_width = label.winfo_reqwidth()
    window_height = label.winfo_reqheight()
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Function to be called when the target text is detected
def on_text_detected(letter):
    show_overlay(letter)

# Function to be called when no target text is detected
def clear_overlay():
    show_overlay("")

# Function to capture the screen and detect text
def detect_text(target_texts, callback, region, sleep_interval=0.5):
    last_detected_text = ""
    while True:
        # Capture the specified region of the screen
        screenshot = pyautogui.screenshot(region=region)
        
        # Convert the image to grayscale
        gray_image = screenshot.convert('L')

        # Use Tesseract to detect text
        detected_text = pytesseract.image_to_string(gray_image)

        # Check if the detected text is different from the last detected text
        if detected_text != last_detected_text:
            last_detected_text = detected_text

            # Check for the "L1" condition using regular expressions
            if re.search(r"EMUMSA-.*?-375", detected_text):
                callback("L1")
            elif re.search(r"EMUMSA-.*?-1376", detected_text):
                callback("L2")
            elif re.search(r"EMUMSA-.*?-1377", detected_text):
                callback("RSC")
            elif re.search(r"EMUMSA-.*?-378", detected_text):
                callback("T1")
            else:
                found = False
                # Check for each target text and call the callback with the corresponding letter
                for target_text, letter in target_texts.items():
                    if target_text in detected_text:
                        callback(letter)
                        found = True
                        break
                
                if not found:
                    clear_overlay()

        time.sleep(sleep_interval)

# Load target texts from CSV file
target_texts = load_target_texts('C:/Users/akio.apollobishwal/Desktop/jojo/trg.csv')

# Run the text detection in a separate thread
thread = threading.Thread(target=detect_text, args=(target_texts, on_text_detected, region, 0.5))
thread.daemon = True
thread.start()

# Keep the Tkinter window open
root.mainloop()
