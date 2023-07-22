import psutil  # Import the psutil library
import time  # Import the time library

# Define a function to get the network IO statistics
def get_net_io_stats():
    # Use the psutil library to get the current network IO statistics
    return psutil.net_io_counters()

# Define a function to print the network IO statistics
def print_net_io_stats(last_stats):
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

    # Update the last network IO statistics
    last_stats = current_stats

# Define the main function
if __name__ == '__main__':
    # Get the initial network IO statistics
    last_stats = get_net_io_stats()

    # Start an infinite loop
    while True:
        # Use the print_net_io_stats function to print the new network IO statistics
        print_net_io_stats(last_stats)

        # Sleep for 1 second
        time.sleep(1)