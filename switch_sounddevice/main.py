from tkinter import Tk, Label, Button, Listbox
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, AudioDeviceState

class AudioDeviceSelector:
    def __init__(self, master):
        self.master = master
        master.title("Select Audio Output Device")

        self.label = Label(master, text="Select the audio device you want to activate:")
        self.label.pack()

        self.listbox = Listbox(master)
        self.listbox.pack()

        self.populate_device_list()

        self.select_button = Button(master, text="Select", command=self.select_device)
        self.select_button.pack()

    def populate_device_list(self):
        # This method correctly fetches and lists active audio devices
        self.audio_devices = AudioUtilities.GetAllDevices()

        max_length = 0  # Variable to store the maximum length of device names

        for device in self.audio_devices:
            print(f"Device: {device.FriendlyName}")
            print(f"  State: {device.state}")
            if device.state == AudioDeviceState.Active:  # DEVICE_STATE_ACTIVE
                device_name = device.FriendlyName
                self.listbox.insert("end", device_name)
                # Update max_length if the current device's name is longer
                if len(device_name) > max_length:
                    max_length = len(device_name)

        # Adjust the width of the listbox to fit the longest device name
        self.listbox.config(width=max_length)

    def select_device(self):
        selection_index = self.listbox.curselection()
        if not selection_index:
            print("No device selected.")
            return

        selected_device = self.audio_devices[selection_index[0]]
        print(f"Selected Device: {selected_device.FriendlyName}")

        # Activating or setting the selected device as default is not straightforward with pycaw
        # and requires additional steps that might involve system settings or other APIs.

def main():
    root = Tk()
    my_gui = AudioDeviceSelector(root)
    root.mainloop()

if __name__ == "__main__":
    main()