import time
import random
from pynput import mouse, keyboard
from pynput.keyboard import Key
import pyautogui  # For simulating tab switching and Num Lock toggle

# Global variables to track user activity and flags
last_activity_time = time.time()
mouse_click_count = 0
keyboard_press_count = 0
action_performed = False  # Flag to control one-time tab switch
toggling_active = False  # Flag to control continuous Num Lock toggling
scroll_direction = "down"
scroll_step_count = 0
max_scroll_steps = 10
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
    ignored_keys = {Key.ctrl, Key.tab, Key.num_lock, Key.space}
    if key in ignored_keys:
        return 
    # if key not in ignored_keys:
    last_activity_time = time.time()
    action_performed = False  # Reset tab-switch action
    toggling_active = False 
    # action_performed = False  # Reset tab-switch action 
    
    keyboard_press_count += 1
    print(f"Key pressed {keyboard_press_count} times.(Key: {key})")

# Register listeners for mouse and keyboard
mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click)
keyboard_listener = keyboard.Listener(on_press=on_press)

mouse_listener.start()
keyboard_listener.start()

try:
    while True:
        # Check the time since the last activity
        current_time = time.time()
        if current_time - last_activity_time > 60:  # No activity for 2 minutes
            if not action_performed:  # Perform tab switch only once per inactivity period
                print("Switching Chrome tab.")
                pyautogui.hotkey('ctrl', 'tab')  # Switch Chrome tabs
                # action_performed = True  # Set flag to prevent repeated tab switching

            if not toggling_active:  # Start toggling loop
                toggling_active = True
                print("User inactive. Starting Num Lock toggling.")

        else:
            # Perform continuous Num Lock toggling while inactive
            if toggling_active:
                print("Toggling Num Lock.")
                pyautogui.press('numlock')  # Toggle Num Lock
                delay = random.uniform(1, 5)  # Generate a random delay between 1 and 5 seconds
                print(f"Delay time: {delay:.2f} seconds")
                time.sleep(delay) # Small delay to simulate toggling

                screen_width, screen_height = pyautogui.size()
                random_x = random.randint(100, screen_width - 100)
                random_y = random.randint(100, screen_height - 100)
                print(f"Moving mouse to ({random_x}, {random_y}).")
                pyautogui.moveTo(random_x, random_y, duration=0.5)

                if scroll_direction == "down":
                    pyautogui.scroll(-500)  # Scroll down
                    print("Scrolling down.")
                else:
                    pyautogui.scroll(500)  # Scroll up
                    print("Scrolling up.")

                scroll_step_count += 1

                if scroll_step_count >= max_scroll_steps:
                    scroll_direction = "up" if scroll_direction == "down" else "down"
                    scroll_step_count = 0  # Reset the counter
                    print(f"Reversing scroll direction to {scroll_direction}.")

                # if pyautogui.position()[1] >= screen_height - 10:  # Near bottom of the screen
                #     scroll_direction = "up"
                # elif pyautogui.position()[1] <= 10:  # Near top of the screen
                #     scroll_direction = "down"
            # pass
            # if toggling_active:  # Stop toggling when user becomes active
            #     print("User active. Stopping Num Lock toggling.")
            #     toggling_active = False

        time.sleep(1)  # Main loop delay
finally:
    mouse_listener.stop()
    keyboard_listener.stop()


# pip install pyinstaller
# pyinstaller --onefile --windowed ts.py # For GUI application
# pyinstaller --onefile ts.py # For console application
# pyinstaller --onefile --windowed --icon=your_icon.ico ts.py # For GUI application with custom icon

