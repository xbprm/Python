import tkinter as tk
import tkinter.simpledialog
import pycaw.pycaw as pycaw
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER

def toggle_specific_window_mute(window_name):
    sessions = pycaw.AudioUtilities.GetAllSessions()
    devices = pycaw.AudioUtilities.GetSpeakers()
    interface = devices.Activate(pycaw.IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = pycaw.AudioUtilities.GetVolumeObject() # cast(interface, POINTER(pycaw.IAudioEndpointVolume))

    for session in sessions:        
        if session.Process and session.Process.name() == window_name:            
            current_mute_state = volume.GetMute()
            print("Toggling Mute State...")
            print("Session: " + session.Process.name())
            print("PID: " + str(session.Process.pid))
            print("Current Mute State: " + str(current_mute_state))
            volume.SetMute(not current_mute_state, session.Process.pid)  # Toggle the mute state

def get_window_name_from_user():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    window_name = tkinter.simpledialog.askstring("Window Name", "Enter the name of the window:")
    return window_name

# Example usage
window_name = get_window_name_from_user()
if window_name:
    toggle_specific_window_mute(window_name)