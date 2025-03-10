import time
from datetime import datetime
from pynput import mouse, keyboard
from pynput.keyboard import Key  # Correct import
import pyautogui  # For simulating tab switching, Num Lock toggle, and screenshots

# Global variables to track user activity and flags
last_activity_time = time.time()
mouse_click_count = 0
keyboard_press_count = 0
action_performed = False  # Flag to control one-time tab switch
toggling_active = False  # Flag to control continuous Num Lock toggling
last_screenshot_time = time.time()  # Track time for taking screenshots

# Function to detect mouse movement
def on_move(x, y):
    global last_activity_time, action_performed, toggling_active
    last_activity_time = time.time()
    action_performed = False  # Reset tab-switch action
    toggling_active = False  # Stop toggling on activity

# Function to detect mouse click
def on_click(x, y, button, pressed):
    global last_activity_time, mouse_click_count, action_performed, toggling_active
    last_activity_time = time.time()
    action_performed = False  # Reset tab-switch action
    toggling_active = False  # Stop toggling on activity
    if pressed:
        mouse_click_count += 1
        print(f"Mouse clicked {mouse_click_count} times.")

# Function to detect keyboard press
def on_press(key):
    global last_activity_time, keyboard_press_count, action_performed, toggling_active
    last_activity_time = time.time()
    ignored_keys = {Key.ctrl, Key.tab, Key.num_lock, Key.space}

    if key not in ignored_keys:
        action_performed = False  # Reset tab-switch action
        toggling_active = False 

    keyboard_press_count += 1
    print(f"Key pressed {keyboard_press_count} times.(Key: {key})")

# Function to take a screenshot
def take_screenshot():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"screenshot_{timestamp}.png"
    pyautogui.screenshot(filename)
    print(f"Screenshot saved: {filename}")

# Register listeners for mouse and keyboard
mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click)
keyboard_listener = keyboard.Listener(on_press=on_press)

mouse_listener.start()
keyboard_listener.start()

try:
    while True:
        # Check the time since the last activity
        current_time = time.time()
        
        # Take a screenshot every 5 minutes
        if current_time - last_screenshot_time > 300:  # 5 minutes (300 seconds)
            take_screenshot()
            last_screenshot_time = current_time  # Update the last screenshot time
        
        if current_time - last_activity_time > 120:  # No activity for 2 minutes
            if not action_performed:  # Perform tab switch only once per inactivity period
                print("Switching Chrome tab.")
                pyautogui.hotkey('ctrl', 'tab')  # Switch Chrome tabs
                action_performed = True  # Set flag to prevent repeated tab switching

            if not toggling_active:  # Start toggling loop
                toggling_active = True
                print("User inactive. Starting Num Lock toggling.")

            # Perform continuous Num Lock toggling while inactive
            if toggling_active:
                print("Toggling Num Lock.")
                pyautogui.press('numlock')  # Toggle Num Lock
                time.sleep(0.5)  # Small delay to simulate toggling
        else:
            if toggling_active:  # Stop toggling when user becomes active
                print("User active. Stopping Num Lock toggling.")
                toggling_active = False

        time.sleep(1)  # Main loop delay
finally:
    mouse_listener.stop()
    keyboard_listener.stop()
