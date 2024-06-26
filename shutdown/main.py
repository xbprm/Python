import tkinter as tk
import os

import tkinter.messagebox as messagebox

# Define the time units
time_units = ["seconds", "minutes", "hours"]
current_unit_index = 1  # Initialize the index to point to the current time unit


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
        confirmation = messagebox.askokcancel("Confirmation", f"Shutdown the system after {duration} {time_units[current_unit_index]}?")
        if confirmation:
            duration_sec = duration * pow(60 , current_unit_index) # Convert minutes to seconds
            print(f"Shutting down after {duration_sec} seconds...")
            print(f"Shutting down after {duration} {time_units[current_unit_index]}...")
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
input_label = tk.Label(root, text=f"Enter the duration in {time_units[current_unit_index]}:")
input_label.pack()
entry = tk.Entry(root)
entry.pack()
entry.focus_set()  # Set focus to the input field

# Function to update the input field with the clicked number
def update_input(number):
    """
    Updates the input field with the number clicked on the keypad.

    This function retrieves the current value from the input field, appends the clicked number to it,
    and then updates the input field with this new value.

    Parameters:
    number (int): The number clicked on the keypad.

    Returns:
    None
    """
    current_value = entry.get()  # Get the current value from the input field
    entry.delete(0, 'end')  # Clear the input field
    entry.insert(0, current_value + str(number))  # Append the clicked number and update the input field

# Create and pack the numerical keypad
keypad_frame = tk.Frame(root)
keypad_frame.pack()

# Add buttons for numbers 0-9
for i in range(1, 10):
    button = tk.Button(keypad_frame, text=str(i), command=lambda num=i: update_input(num))
    button.grid(row=(i-1)//3, column=(i-1)%3)

# Add button for number 0
button_0 = tk.Button(keypad_frame, text="0", command=lambda: update_input(0))
button_0.grid(row=3, column=1)

# Bind the Enter key to the shutdown action
entry.bind("<Return>", shutdown_after_duration)

# Function to delete the last number entered
def delete_last():
    """
    Deletes the last character entered in the input field.

    This function retrieves the current value from the input field, calculates the length of this string,
    and then deletes the last character by adjusting the end index of the string in the input field.

    Parameters:
    None

    Returns:
    None
    """
    current_value = entry.get()  # Get the current value from the input field
    entry.delete(len(current_value) - 1, 'end')  # Delete the last character

# Create and pack the delete button
delete_button = tk.Button(root, text="Delete", command=delete_last)
delete_button.pack()

# Function to clear the input field
def clear_input():
    """
    Clears the input field in the GUI.

    This function deletes all the current content from the entry widget, effectively resetting it to an empty state.

    Parameters:
    None

    Returns:
    None
    """
    entry.delete(0, 'end')  # Delete all content from the beginning (0) to the end of the entry widget

# Create and pack the clear button
clear_button = tk.Button(root, text="Clear", command=clear_input)
clear_button.pack()

# Function to switch between hours, minutes, and seconds
def switch_time_unit():
    """
    Switches the current time unit among seconds, minutes, and hours in a cyclic manner.

    This function updates the global variable `current_unit_index` to cycle through the indices
    corresponding to the time units defined in the `time_units` list. It then updates the input label
    to reflect the newly selected time unit and clears the input field to prompt the user for a new value
    in the context of the selected time unit.

    Parameters:
    None

    Returns:
    None
    """
    global current_unit_index  # Access the global variable to track the current time unit index
    current_unit_index = (current_unit_index + 1) % len(time_units)  # Cycle through the time units
    selected_unit = time_units[current_unit_index]  # Get the currently selected time unit
    input_label.config(text=f"Enter the duration in {selected_unit}:")  # Update the input label
    entry.delete(0, 'end')  # Clear the input field to prompt for new input  # Clear the input field
    # entry.insert(0, f"Enter the duration in {selected_unit}")  # Set the input field placeholder

# Create and pack the button to switch between hours, minutes, and seconds
switch_button = tk.Button(root, text="Switch Time Unit", command=switch_time_unit)
switch_button.pack()

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