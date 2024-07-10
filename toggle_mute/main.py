import tkinter as tk
import tkinter.simpledialog
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

def toggle_specific_window_mute(window_names):
    """
    Toggles the mute state of specific windows/applications based on their names.

    This function iterates over a list of window names, finds the corresponding audio session
    for each window, and toggles its mute state. It uses the pycaw library to interact with
    the audio sessions.

    Parameters:
    - window_names (list of str): A list of window names (as strings) whose mute state is to be toggled.

    Returns:
    - None
    """
    sessions = AudioUtilities.GetAllSessions()

    for window_name in window_names:  # Iterate over each window name in the list
        for session in sessions:
            if session.Process and session.Process.name() == window_name:
                simple_volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                current_mute_state = simple_volume.GetMute()
                print("Toggling Mute State...")
                print("Session: " + session.Process.name())
                print("PID: " + str(session.Process.pid))
                print("Current Mute State: " + str(current_mute_state))
                simple_volume.SetMute(not current_mute_state, None)  # Toggle the mute state

root = tk.Tk()
root.withdraw()  # Hide the root window

selection_window = tk.Toplevel(root)
selection_window.title("Select Window")

# Instead of Listbox, use a frame to contain Checkbuttons
checkbox_frame = tk.Frame(selection_window)
checkbox_frame.pack()

window_checkboxes = []
window_names_vars = {}

def update_window_list():
    """
    Updates the list of window names displayed as Checkbuttons in the GUI.

    This function first clears any existing Checkbuttons in the checkbox_frame. It then retrieves
    the current list of open window names using the pycaw library to access audio sessions. Duplicate
    window names are removed to ensure each window is only listed once. For each unique window name,
    a Checkbutton is created and added to the checkbox_frame, allowing the user to select which windows
    to toggle mute on.

    Parameters:
    - None

    Returns:
    - None
    """
    # Clear existing checkboxes
    for widget in checkbox_frame.winfo_children():
        widget.destroy()

    # Retrieve the latest list of open window names, removing duplicates
    window_names = [session.Process.name() for session in AudioUtilities.GetAllSessions() if session.Process]
    window_names = list(dict.fromkeys(window_names))  # Remove duplicates

    # Create a Checkbutton for each window name and add it to the GUI
    for name in window_names:
        var = tk.BooleanVar()
        chk = tk.Checkbutton(checkbox_frame, text=name, variable=var)
        chk.pack(anchor='w')
        window_checkboxes.append(chk)
        window_names_vars[name] = var

update_window_list()  # Initial population of the window list

# Refresh button to update the list of open windows
refresh_button = tk.Button(selection_window, text="Refresh", command=update_window_list)
refresh_button.pack()

def on_toggle_mute():
    """
    Handles the mute toggling action for selected windows.

    This function retrieves the names of windows selected by the user through the GUI, toggles their mute state,
    and then resets the selection. It uses the global `selected_windows` variable to store the current selection,
    calls `toggle_specific_window_mute` to apply the mute state toggle, and finally resets the Checkbutton states
    in the GUI to reflect that the action has been completed.

    Parameters:
    - None

    Returns:
    - None
    """
    # Retrieve selected window names based on Checkbutton states
    selected_window_names = [name for name, var in window_names_vars.items() if var.get()]
    global selected_windows
    selected_windows = selected_window_names
    toggle_specific_window_mute(selected_windows)  # Toggle the mute state for selected windows
    # Clear the selection by resetting each BooleanVar for next use
    for var in window_names_vars.values():
        var.set(False)

toggle_mute_button = tk.Button(selection_window, text="Toggle Mute", command=on_toggle_mute)
toggle_mute_button.pack()

def exit_application():
    """
    Closes the application by destroying the root Tkinter window.

    This function is bound to the Exit button in the GUI. When invoked, it terminates the application
    by calling the `destroy` method on the global `root` Tkinter object, effectively closing the main
    application window and stopping the Tkinter main loop.

    Parameters:
    - None

    Returns:
    - None
    """
    root.destroy()

exit_button = tk.Button(selection_window, text="Exit", command=exit_application)
exit_button.pack()

# Run the main loop
root.mainloop()