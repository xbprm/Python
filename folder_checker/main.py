import os
import time
import psutil
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon

# Define path of the file where the last execution size is stored    
last_execution_size_folder = os.path.join(os.path.expanduser("~"), ".folder_change_notifier")
last_execution_size_file = os.path.join(last_execution_size_folder, "last_execution_size.txt")

# Define the path to the folder to be monitored
folder_path = r"D:\Videos\Porn\unclassified"

# Define the message to be posted in the system tray
message = "Contents of folder have changed!"

# Define the function to be called when the contents of the folder change
def check_folder_changes():
    # Get the size of the folder when the script was last executed
    last_execution_size = get_last_execution_size()

    # Get the current size of the folder
    current_size = get_folder_size(folder_path)

    # Check if the sizes are different
    print("Current size: " + str(current_size)) 
    print("Last execution size: " + str(last_execution_size))
    if current_size != last_execution_size:
        # Post the message in the system tray
        print(message)
        post_message(message)
    else:
        print("The size of the folder has not changed!")
        
# Define the function to get the size of the folder
def get_folder_size(folder_path):
    # Initialize the size to 0
    size = 0
    
    # Get the list of files in the folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Calculate the size of the file
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            size += file_size

    if not os.path.exists(last_execution_size_folder):
        os.makedirs(last_execution_size_folder, exist_ok=True)

    with open(last_execution_size_file, "w") as file:
        file.write(str(size))
        
    # Return the size
    return size

# Define the function to get the size of the folder when the script was last executed
def get_last_execution_size():
    # Check if the file exists
    if os.path.exists(last_execution_size_file):
        # Read the last execution size from the file
        with open(last_execution_size_file, "r") as file:
            last_execution_size = int(file.read())
    else:
        # The file does not exist, so set the last execution size to 0
        last_execution_size = 0
    
    # Return the last execution size
    return last_execution_size

# Define the function to post a message in the system tray
def post_message(message):
    # Initialize the tray icon
    # tray_icon = QSystemTrayIcon(QIcon("icon.png")) # , "Folder Change Notifier")
    # tray_icon.show()
    
    # # Initialize the menu
    # menu = QMenu()
    # action = QAction(message, tray_icon)
    # menu.addAction(action)
    
    # # Connect the action to the system tray
    # tray_icon.setContextMenu(menu)
    # tray_icon.activated.connect(menu.popup)

    print(message)

if __name__ == "__main__":

    # Start the monitoring process
    check_folder_changes()

    # Start an infinite loop to continuously monitor the folder changes
    while True:
        # Check if the contents of the folder have changed
        check_folder_changes()
        
        # Sleep for 1 minute
        time.sleep(5)
