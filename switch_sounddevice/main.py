from tkinter import Tk, Label, Button, Listbox
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, AudioDeviceState

class AudioDeviceSelector:
    def __init__(self, master):
        """
        Initialize the AudioDeviceSelector application window.

        This method sets up the GUI components for the application, including a label, a listbox for displaying audio devices,
        and a select button to activate the chosen device. It also triggers the population of the audio devices list.

        Parameters:
        - master: The parent window for the AudioDeviceSelector application.

        Returns:
        None
        """
        self.master = master
        master.title("Select Audio Output Device")  # Set the window title

        # Create and pack a label widget into the master widget
        self.label = Label(master, text="Select the audio device you want to activate:")
        self.label.pack()

        # Create and pack a listbox widget for listing audio devices
        self.listbox = Listbox(master)
        self.listbox.pack()

        # Populate the listbox with available audio devices
        self.populate_device_list()

        # Create and pack a button widget for selecting an audio device
        self.select_button = Button(master, text="Select", command=self.select_device)
        self.select_button.pack()

    def populate_device_list(self):
        """
        Populates the listbox with the names of active audio devices.

        This method fetches all available audio devices using the AudioUtilities.GetAllDevices method from the pycaw library.
        It then iterates through these devices, filtering for those that are in an 'Active' state, and inserts their friendly names
        into the listbox widget for user selection. Additionally, it adjusts the width of the listbox to accommodate the longest
        device name, ensuring all device names are fully visible without truncation.

        Parameters:
        None

        Returns:
        None
        """
        self.audio_devices = AudioUtilities.GetAllDevices()  # Fetch all available audio devices

        max_length = 0  # Variable to store the maximum length of device names

        for device in self.audio_devices:
            print(f"Device: {device.FriendlyName}")  # Debug print the device's friendly name
            print(f"  State: {device.state}")  # Debug print the device's state
            if device.state == AudioDeviceState.Active:  # Check if the device is in 'Active' state
                device_name = device.FriendlyName  # Get the device's friendly name
                self.listbox.insert("end", device_name)  # Insert the device name into the listbox
                # Update max_length if the current device's name is longer
                if len(device_name) > max_length:
                    max_length = len(device_name)

        # Adjust the width of the listbox to fit the longest device name
        self.listbox.config(width=max_length)

    def select_device(self):
        """
        Selects the audio device based on the user's choice from the listbox.

        This method retrieves the index of the currently selected item in the listbox,
        checks if a selection has been made, and then prints the friendly name of the
        selected audio device. It is designed to be called when the user clicks the
        'Select' button.

        Parameters:
        None

        Returns:
        None
        """
        selection_index = self.listbox.curselection()  # Get the index of the selected item
        if not selection_index:  # Check if a selection has been made
            print("No device selected.")  # Inform the user if no selection was made
            return

        selected_device = self.audio_devices[selection_index[0]]  # Retrieve the selected device from the list of devices
        print(f"Selected Device: {selected_device.FriendlyName}")  # Print the friendly name of the selected device

        # Activating or setting the selected device as default is not straightforward with pycaw
        # and requires additional steps that might involve system settings or other APIs.

def main():
    """
    The main function of the application.

    This function initializes the main application window using Tkinter, creates an instance of the AudioDeviceSelector class,
    and enters the Tkinter event loop. This setup is necessary for the GUI to respond to user interactions such as button clicks
    and selections from the list.

    Parameters:
    None

    Returns:
    None
    """
    root = Tk()  # Initialize the main application window
    my_gui = AudioDeviceSelector(root)  # Create an instance of the AudioDeviceSelector class
    root.mainloop()  # Enter the Tkinter event loop to keep the application running and responsive

if __name__ == "__main__":
    main()