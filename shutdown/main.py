import tkinter as tk
import os

import tkinter.messagebox as messagebox

def shutdown_after_duration(event=None):
    """
    Initiates a system shutdown after a specified duration, displaying a confirmation dialog.

    This function retrieves the duration in minutes from the input field, converts it to seconds,
    and displays a confirmation dialog before scheduling a system shutdown after the specified duration.
    If the input is invalid, it displays an error message.

    Parameters:
    event (tk.Event, optional): The event object (default is None)

    Returns:
    None
    """
    try:
        duration = int(entry.get())  # Retrieve the duration in minutes from the input field
        confirmation = messagebox.askokcancel("Confirmation", f"Shutdown the system after {duration} minutes?")
        if confirmation:
            duration_sec = duration * 60  # Convert minutes to seconds
            print(f"Shutting down after {duration} minutes...")
            os.system(f"shutdown /s /t {duration_sec}")  # Schedule a system shutdown
            root.destroy()  # Terminate the GUI application
    except ValueError:
        result_label.config(text="Invalid input. Please enter a valid number.")  # Display error message for invalid input

def abort_shutdown():
    """
    Aborts the scheduled system shutdown.

    This function sends a command to the operating system to abort the scheduled system shutdown.

    Parameters:
    None

    Returns:
    None
    """
    print("Aborting shutdown...")
    os.system("shutdown /a")  # Abort the computer shutdown  # Abort the computer shutdown

# Create the main window
root = tk.Tk()
root.title("Shutdown After Duration")

# Create and pack the input label and entry
input_label = tk.Label(root, text="Enter the duration in minutes:")
input_label.pack()
entry = tk.Entry(root)
entry.pack()
entry.focus_set()  # Set focus to the input field

# Bind the Enter key to the shutdown action
entry.bind("<Return>", shutdown_after_duration)

# Create and pack the button to trigger the shutdown
shutdown_button = tk.Button(root, text="Shutdown", command=shutdown_after_duration)
shutdown_button.pack()

# Create and pack the button to abort the shutdown
abort_button = tk.Button(root, text="Abort Shutdown", command=abort_shutdown)
abort_button.pack()

# Create and pack the label for displaying error messages
result_label = tk.Label(root, text="")
result_label.pack()

# Run the main loop
root.mainloop()