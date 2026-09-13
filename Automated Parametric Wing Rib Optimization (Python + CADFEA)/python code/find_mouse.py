import pyautogui
import time

print(">>> You have 5 seconds to hover your mouse over the target button! <<<")
for i in range(5, 0, -1):
    print(f"{i}...")
    time.sleep(1)

# Grab the location
x, y = pyautogui.position()
print(f"\nSUCCESS! The coordinates are: x={x}, y={y}")