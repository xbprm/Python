import tkinter as tk
import tkinter.simpledialog
from comtypes import CLSCTX_ALL
import pycaw.pycaw as pycaw
from ctypes import cast, POINTER

def toggle_specific_window_mute(window_name):
    sessions = pycaw.AudioUtilities.GetAllSessions()

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
    window_name = tkinter.simpledialog.askstring("Window Name", "Enter the name of the window:")
    return window_name

if __name__ == "__main__":
    window_name = get_window_name_from_user()
    if window_name:
        toggle_specific_window_mute(window_name)