import tkinter as tk
import tkinter.simpledialog
from comtypes import CLSCTX_ALL
import pycaw.pycaw as pycaw
from ctypes import cast, POINTER

def toggle_specific_window_mute(window_names):
    sessions = pycaw.AudioUtilities.GetAllSessions()

    for window_name in window_names:  # Iterate over each window name in the list
        for session in sessions:
            if session.Process and session.Process.name() == window_name:
                simple_volume = session._ctl.QueryInterface(pycaw.ISimpleAudioVolume)
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
    # Clear existing checkboxes
    for widget in checkbox_frame.winfo_children():
        widget.destroy()
    
    # Retrieve the latest list of open window names
    window_names = [session.Process.name() for session in pycaw.AudioUtilities.GetAllSessions() if session.Process]
    window_names = list(dict.fromkeys(window_names))  # Remove duplicates

    # Create a Checkbutton for each window name
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
    # Retrieve selected window names based on Checkbutton states
    selected_window_names = [name for name, var in window_names_vars.items() if var.get()]
    global selected_windows
    selected_windows = selected_window_names
    toggle_specific_window_mute(selected_windows)
    # Optionally, reset Checkbuttons here for next use or handle window hiding/showing
    # Clear the selection by resetting each BooleanVar
    for var in window_names_vars.values():
        var.set(False)

toggle_mute_button = tk.Button(selection_window, text="Toggle Mute", command=on_toggle_mute)
toggle_mute_button.pack()

def exit_application():
    root.destroy()

exit_button = tk.Button(selection_window, text="Exit", command=exit_application)
exit_button.pack()

# Run the main loop
root.mainloop()