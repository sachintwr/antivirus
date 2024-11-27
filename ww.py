import time
import pygetwindow as gw  # To detect active windows
import pyautogui  # To simulate keypresses and mouse clicks

# The title or part of the title of the app window you want to detect
TARGET_WINDOW_TITLE = "WaitingWindow"  # Replace with the actual title of the app

try:
    while True:
        # Get the active window
        active_window = gw.getActiveWindow()
        if active_window:
            window_title = active_window.title

            # Check if the target app's window is active
            if TARGET_WINDOW_TITLE in window_title:
                print(f"Detected target window: {window_title}")

                # Get the position and size of the target window
                left, top, width, height = active_window.left, active_window.top, active_window.width, active_window.height
                print(f"Window position: left={left}, top={top}, width={width}, height={height}")

                # Calculate the position of the close button (usually top-right corner)
                close_button_x = left + (width // 2)  # Adjust -20 based on close button padding
                close_button_y = top + height - 30   # Adjust +10 based on close button vertical position

                # Simulate a mouse click on the close button
                pyautogui.moveTo(close_button_x, close_button_y, duration=0.5)  # Smooth movement to the close button
                pyautogui.click()
                print("Clicked on the close button.")
                
                # Exit loop after closing the window (if desired)
                time.sleep(5) 
                # break
            else:
                print(f"Active window is not target: {window_title}")
        else:
            print("No active window detected.")

        time.sleep(1)  # Check every second

except KeyboardInterrupt:
    print("Script stopped.")
