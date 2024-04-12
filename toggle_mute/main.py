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

def get_window_name_from_user():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    selection_window = tk.Toplevel(root)
    selection_window.title("Select Window")

    # Use a Listbox for multiple selections
    listbox = tk.Listbox(selection_window, selectmode='multiple')
    listbox.pack()

    def update_window_list():
        # Retrieve the latest list of open window names
        window_names = [session.Process.name() for session in pycaw.AudioUtilities.GetAllSessions() if session.Process]
        window_names = list(dict.fromkeys(window_names))  # Remove duplicates

        # Update the Listbox
        listbox.delete(0, 'end')
        for name in window_names:
            listbox.insert('end', name)

    update_window_list()  # Initial population of the window list

    # Refresh button to update the list of open windows
    refresh_button = tk.Button(selection_window, text="Refresh", command=update_window_list)
    refresh_button.pack()

    def on_ok():
        # Retrieve selected window names
        selected_indices = listbox.curselection()
        selected_window_names = [listbox.get(i) for i in selected_indices]
        global selected_windows  # Use a global variable or better, return this list if modifying function structure
        selected_windows = selected_window_names
        selection_window.destroy()  # Close the selection window

    ok_button = tk.Button(selection_window, text="OK", command=on_ok)
    ok_button.pack()

    selection_window.wait_window()  # Wait for the selection window to close

    # Return the list of selected window names
    return selected_windows

if __name__ == "__main__":
    window_name = get_window_name_from_user()
    if window_name:
        toggle_specific_window_mute(window_name)