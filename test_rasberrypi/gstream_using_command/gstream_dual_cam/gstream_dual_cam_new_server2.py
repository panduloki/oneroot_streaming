import subprocess
import threading
import atexit
import psutil  # Make sure to install psutil (`pip install psutil`)

# List to keep track of processes and threads
processes = []
threads = []


def get_gstreamer_process_count():
    """
    Counts the number of running GStreamer processes.
    """
    count = 0
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        try:
            if 'gst' in proc.info['name'].lower():
                count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return count


def terminate_gstreamer_processes():
    """
    Terminates all running GStreamer processes.
    """
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        try:
            if 'gst' in proc.info['name'].lower():
                print(f"Terminating GStreamer process with PID {proc.info['pid']}...")
                proc.terminate()  # Sends a terminate signal
                proc.wait(timeout=5)  # Wait up to 5 seconds for process to terminate
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
        except psutil.TimeoutExpired:
            print(f"Process {proc.info['pid']} did not terminate in time; force killing...")
            proc.kill()


def cleanup():
    """
    Gracefully terminate all running processes and threads.
    """
    # Kill all processes
    for process in processes:
        if process.is_alive():
            print(f"Terminating process {process.name}...")
            process.terminate()
            process.join()
            print(f"Process {process.name} terminated.")

    # Stop all threads (note: threads can't be forcefully killed, so ensure safe exit)
    for thread in threads:
        if thread.is_alive():
            print(f"Waiting for thread {thread.name} to finish...")
            thread.join()
            print(f"Thread {thread.name} finished.")


# Register the cleanup function to run on exit
atexit.register(cleanup)


def start_camera_stream(device: str, host: str, port: int):
    """
    Starts a camera stream using GStreamer.

    Args:
        device (str): The camera device path (e.g., "/dev/video0").
        host (str): The IP address of the host to send the stream to.
        port (int): The port for the UDP stream.
    """
    # Check and terminate any running GStreamer processes before starting a new one
    if get_gstreamer_process_count() > 0:
        print("Existing GStreamer processes found. Terminating them...")
        terminate_gstreamer_processes()

    gst_command = [
        "gst-launch-1.0",
        "v4l2src", f"device={device}",
        "!", "video/x-raw,width=640,height=480,framerate=30/1",
        "!", "videoconvert",
        "!", "x264enc", "tune=zerolatency", "bitrate=500",
        "!", "rtph264pay", "config-interval=1", "pt=96",
        "!", "udpsink", f"host={host}", f"port={port}"
    ]

    try:
        print(f"Starting camera stream from {device} to {host}:{port}...")
        process = subprocess.Popen(gst_command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        processes.append(process)  # Add process to the list for cleanup
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            print(f"Error occurred while streaming from {device}: {stderr.decode()}")
        else:
            print(f"Camera stream from {device} started successfully.")
    except FileNotFoundError:
        print("Error: GStreamer is not installed or `gst-launch-1.0` is not available in PATH.")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")


def main():
    jetson_nano_ip = "100.71.196.8"
    port0 = 5000
    port1 = 5001

    # Create and start threads
    thread0 = threading.Thread(target=start_camera_stream, args=("/dev/video0", jetson_nano_ip, port0), name="Camera0")
    thread1 = threading.Thread(target=start_camera_stream, args=("/dev/video2", jetson_nano_ip, port1), name="Camera1")

    threads.extend([thread0, thread1])  # Add threads to the list for cleanup

    # Start the threads
    thread0.start()
    thread1.start()

    # Wait for threads to complete
    thread0.join()
    thread1.join()


if __name__ == "__main__":
    main()
