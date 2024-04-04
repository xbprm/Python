import tkinter as tk
import os

def shutdown_after_duration():
    try:
        duration = int(entry.get())
        duration_sec = duration * 60  # Convert minutes to seconds
        print(f"Shutting down after {duration} minutes...")
        os.system(f"shutdown /s /t {duration_sec}")  # Shutdown the computer
        root.destroy()  # Terminate the GUI application
    except ValueError:
        result_label.config(text="Invalid input. Please enter a valid number.")

# Create the main window
root = tk.Tk()
root.title("Shutdown After Duration")

# Create and pack the input label and entry
input_label = tk.Label(root, text="Enter the duration in minutes:")
input_label.pack()
entry = tk.Entry(root)
entry.pack()

# Create and pack the button to trigger the shutdown
shutdown_button = tk.Button(root, text="Shutdown", command=shutdown_after_duration)
shutdown_button.pack()

# Create and pack the label for displaying error messages
result_label = tk.Label(root, text="")
result_label.pack()

# Run the main loop
root.mainloop()