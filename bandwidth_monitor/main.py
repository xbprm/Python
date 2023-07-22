import psutil  # Import the psutil library
import time  # Import the time library

# Get the current network IO statistics
last_received = psutil.net_io_counters().bytes_recv  # last_received = psutil.net_io_counters()["bytes_recv"]
last_sent = psutil.net_io_counters().bytes_sent  # last_sent = psutil.net_io_counters()["bytes_sent"]
last_total = last_received + last_sent

# Start an infinite loop
while True:
    # Get the current network IO statistics
    bytes_received = psutil.net_io_counters().bytes_recv  # bytes_received = psutil.net_io_counters()["bytes_recv"]
    bytes_sent = psutil.net_io_counters().bytes_sent  # bytes_sent = psutil.net_io_counters()["bytes_sent"]
    bytes_total = bytes_received + bytes_sent

    # Calculate the new network IO statistics
    new_received = bytes_received - last_received  # new_received = bytes_received - last_received
    new_sent = bytes_sent - last_sent  # new_sent = bytes_sent - last_sent
    new_total = bytes_total - last_total  # new_total = bytes_total - last_total

    # Convert the new network IO statistics to MB/s
    mb_new_received = new_received / 1024 / 1024  # mb_new_received = new_received / (1024 * 1024)
    mb_new_sent = new_sent / 1024 / 1024  # mb_new_sent = new_sent / (1024 * 1024)
    mb_new_total = new_total / 1024 / 1024  # mb_new_total = new_total / (1024 * 1024)

    # Print the new network IO statistics
    print(f"Received: {mb_new_received:.2f} MB/s, Sent: {mb_new_sent:.2f} MB/s, Total: {mb_new_total:.2f} MB/s")

    # Update the last network IO statistics
    last_received = bytes_received
    last_sent = bytes_sent
    last_total = bytes_total

    # Sleep for 1 second
    time.sleep(1)