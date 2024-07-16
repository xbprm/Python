import psutil  # Import the psutil library
import time  # Import the time library
import matplotlib.pyplot as plt  # Import the matplotlib library
import socket
import tkinter as tk  # Import the Tkinter library
from tkinter import messagebox  # Import the messagebox module from Tkinter

SHOW_PLOT = False
UPDATE_FREQUENCY = 0.001  # Update frequency in seconds

# Define a function to get the network IO statistics
def get_net_io_stats():
    # Use the psutil library to get the current network IO statistics
    return psutil.net_io_counters()

# Define a function to print the network IO statistics
def print_net_io_stats(last_stats, x_values, y_values):
    # Use the get_net_io_stats function to get the current network IO statistics
    current_stats = get_net_io_stats()

    # Calculate the new network IO statistics
    new_received = current_stats.bytes_recv - last_stats.bytes_recv
    new_sent = current_stats.bytes_sent - last_stats.bytes_sent
    new_total = new_received + new_sent

    # Convert the new network IO statistics to MB/s
    mb_new_received = new_received / 1024 / 1024
    mb_new_sent = new_sent / 1024 / 1024
    mb_new_total = new_total / 1024 / 1024

    # Print the new network IO statistics
    print(f"Received: {mb_new_received:.2f} MB/s, Sent: {mb_new_sent:.2f} MB/s, Total: {mb_new_total:.2f} MB/s")

    if SHOW_PLOT:
        # Update the data for the plot
        x_values.append(len(x_values))
        y_values.append(mb_new_total)

        # Clear the plot
        plt.clf()

        # Plot the data
        plt.plot(x_values, y_values, label="Total MB/s")

        # Set the plot title and labels
        plt.title("Network IO Statistics")
        plt.xlabel("Time (seconds)")
        plt.ylabel("MB/s")

        # Add a legend
        plt.legend()

        # Draw the plot
        plt.pause(UPDATE_FREQUENCY)

    # Update the last network IO statistics
    return current_stats

# Define the main function
if __name__ == '__main__':

    # Create a Tkinter window
    root = tk.Tk()
    root.withdraw()  # Hide the Tkinter window

    # Ask the user if the plot should be shown
    show_plot_choice = messagebox.askyesno("Plot Visibility", "Do you want to show the plot?")
    SHOW_PLOT = show_plot_choice

    # Get the hostname
    hostname = socket.gethostname()

    if hostname == "FRLCHBWW":
        UPDATE_FREQUENCY = 1  # Update frequency in seconds

    # Get the initial network IO statistics
    last_stats = get_net_io_stats()

    # Initialize the data for the plot
    x_values = []
    y_values = []

    # Start an infinite loop
    while True:
        # Use the print_net_io_stats function to print the new network IO statistics
        current_stats = print_net_io_stats(last_stats, x_values, y_values)
        last_stats = current_stats

        # Sleep for 1 second
        time.sleep(1)