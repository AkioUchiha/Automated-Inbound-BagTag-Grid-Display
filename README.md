# Automated-Inbound-BagTag-Grid-Display
This Python program allows users to select two points on the screen, defining a rectangular region. The program continuously takes screenshots of the defined region every 0.5 seconds, detects text within the area, and checks for a corresponding grid letter in a CSV file.

Features:

Region Selection: Users can select two points on the screen, specifying the top-left and bottom-right corners of the rectangle.

Text Detection: Text within the rectangle is detected in real-time using OCR (Optical Character Recognition).

CSV Lookup: The detected text is searched in a CSV file, and if a match is found, the corresponding grid letter (from the adjacent column) is displayed as an overlay on the screen.

Real-time Overlay: The grid letter is shown as an overlay on the screen and vanishes after a few seconds. If no match is found in the CSV file, no overlay is displayed.

Continuous Updates: The program takes new screenshots every 0.5 seconds for real-time updates.

Libraries Used:

pyautogui for capturing screenshots
csv module for reading the CSV file
tkinter for overlay display
pynput for screen coordinate selection
pytesseract for text detection (OCR)
This program is ideal for use cases where real-time screen text needs to be detected and matched with predefined data, with results dynamically displayed on the screen.
