import time
import tkinter as tk
from PIL import ImageGrab
import basic_registration_form

root = basic_registration_form.App()
root.update_idletasks()
root.update()
# make sure window is visible
root.deiconify()
root.lift()
root.focus_force()
root.update_idletasks()
root.update()

# wait a moment for the window to render fully
root.after(500, lambda: None)
time.sleep(0.5)

x = root.winfo_rootx()
y = root.winfo_rooty()
w = root.winfo_width()
h = root.winfo_height()
img = ImageGrab.grab(bbox=(x, y, x+w, y+h))
img.save('screenshots/basic_form.png')
print(f'Screenshot saved to screenshots/basic_form.png ({w}x{h})')
root.destroy()
