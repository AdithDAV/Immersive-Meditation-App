import tkinter as tk
from tkinter import messagebox
import subprocess  # Import subprocess to run an external script

def open_guided_narration():
    # Placeholder function to open the Guided Narration page
    # messagebox.showinfo("Navigate", "Navigating to Guided Narration Page")
    subprocess.run(["python", "guidedNarration.py"], check=True)

def open_enjoy_nature():
    # Function to run the nature_canvas.py script
    subprocess.Popen(['python3', 'nature_canvas.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    subprocess.Popen(['python3', 'updateAudioHRTF.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


    # subprocess.run(["python3", "nature_canvas.py"], check=True)
    # subprocess.run(["python3", "updateAudioHRTF.py"], check=True)

# Create the main window
root = tk.Tk()
root.title("Immersive Meditation Application")

# Set the window size (width x height)
root.geometry("400x200")

# Greeting message
greeting = tk.Label(root, text="Welcome to the Immersive Meditation Application!", font=("Arial", 12))
greeting.pack(pady=10)

# Title for the options
option_title = tk.Label(root, text="Select any option", font=("Arial", 12, "bold"))
option_title.pack(pady=10)

# Buttons
guided_button = tk.Button(root, text="Guided Narration", command=open_guided_narration)
guided_button.pack(pady=(0, 10))

nature_button = tk.Button(root, text="Enjoy The Nature", command=open_enjoy_nature)
nature_button.pack(pady=(0, 10))

# Start the GUI
root.mainloop()