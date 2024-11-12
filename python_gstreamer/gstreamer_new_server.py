import gi
import socket
import signal
import subprocess  # To run the loclx tunnel

# Ensure the correct GStreamer versions are loaded
try:
    gi.require_version('Gst', '1.0')
    gi.require_version('GstRtspServer', '1.0')
    from gi.repository import Gst, GstRtspServer, GObject
except ValueError as e:
    print("Error:", e)
    print("Make sure GStreamer and GstRtspServer are properly installed.")
    exit(1)

def get_local_ip():
    """Retrieve the local IP address of the machine."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print("Could not determine local IP address:", e)
        return "localhost"

# Initialize GStreamer
try:
    Gst.init(None)
    print("GStreamer initialized.")
except Exception as e:
    print("Failed to initialize GStreamer:", e)
    exit(1)

class RtspServer(GstRtspServer.RTSPServer):
    def __init__(self):
        super(RtspServer, self).__init__()
        print("Setting up RTSP server...")
        
        # Create the RTSP Media Factory for streaming
        self.factory = GstRtspServer.RTSPMediaFactory()
        
        # Set the pipeline for capturing and encoding video from the USB camera
        self.factory.set_launch("( v4l2src device=/dev/video0 ! videoconvert ! video/x-raw,width=640,height=480,format=I420 ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay name=pay0 pt=96 )")
        
        # Allow shared access to this media
        self.factory.set_shared(True)
        
        # Add the media factory to the server's mount points (this defines the stream URL)
        self.get_mount_points().add_factory("/test", self.factory)
        
        # Attach the server
        self.attach(None)
        
        # Print the local IP address for accessing the stream
        local_ip = get_local_ip()
        print("RTSP server is ready and streaming on rtsp://"+local_ip+":8554/test")
        
        # Start `loclx` to expose the RTSP stream publicly
        self.start_loclx_tunnel()

    def start_loclx_tunnel(self):
    	"""Start `loclx` tunnel to expose the RTSP server and print tunnel information."""
    	try:
        	print("Starting loclx tunnel to expose RTSP stream...")

        	# Start the loclx tunnel, exposing the RTSP stream via TCP
        	loclx_process = subprocess.Popen(
            	["loclx", "tunnel", "http", "--to", "localhost:8554"],  # Using TCP for RTSP
            	stdout=subprocess.PIPE, stderr=subprocess.PIPE
        	)

        	# Capture the output of loclx (both stdout and stderr)
        	stdout, stderr = loclx_process.communicate()

        	# Decode the stdout and stderr
        	stdout_decoded = stdout.decode('utf-8')
        	stderr_decoded = stderr.decode('utf-8')

        	# Print raw output to debug
        	print("loclx stdout:", stdout_decoded)
        	print("loclx stderr:", stderr_decoded)

        	# Check if tunnel creation was successful
        	if "Tunnel created:" in stdout_decoded:
            		# Extract and print the tunnel information
            		tunnel_url = stdout_decoded.split("Tunnel created:")[1].strip()
            		print("Tunnel created using TCP. Public RTSP URL: rtsp://"+tunnel_url+"/test")
        	else:
            		print("Failed to create loclx tunnel.")
            		print("Error details:", stderr_decoded)

    	except Exception as e:
        	print("Error starting loclx tunnel:", e)


    def shutdown(self):
        """Gracefully shutdown the RTSP server."""
        print("Shutting down the RTSP server...")
        self.get_context().quit()  # Stops the GObject main loop
        self.release()  # Release any resources associated with the RTSP server

# Function to handle the interrupt signal (Ctrl+C)
def signal_handler(sig, frame):
    print("ctrl+c Interrupt received in terminal, shutting down...")
    server.shutdown()  # Call shutdown method to gracefully close the stream
    exit(0)

# Register the signal handler to catch SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    try:
        # Start the RTSP server and run the GObject main loop to handle requests
        server = RtspServer()
        print("Starting GObject Main Loop...")
        loop = GObject.MainLoop()
        loop.run()  # Starts the main event loop, listening for client requests
    
    except KeyboardInterrupt:
        print("\nReceived keyboard interrupt, shutting down the server...")
        server.shutdown()  # Gracefully shut down the server
        exit(0)  # Exit cleanly
        
    except Exception as e:
        print("An error occurred:", e)
        if 'server' in locals():
            server.shutdown()  # Ensure the server is shut down on error
        print("Exiting...")
        exit(1)

