import gi
import socket  # Import socket module here
import signal  # To handle shutdown signals

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
        # Create a socket connection to an external server to determine the local IP (doesn't actually send data)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google DNS server
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print("Could not determine local IP address:", e)
        return "localhost"  # Default to localhost in case of error

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
        print("\n Received keyboard interrupt, shutting down the server...")
        server.shutdown()  # Gracefully shut down the server
        exit(0)  # Exit cleanly
        
    except Exception as e:
        # Handle unexpected errors and ensure the server shuts down gracefully
        print("An error occurred:", e)
        if 'server' in locals():
            server.shutdown()  # Ensure the server is shut down on error
        print("Exiting...")
        exit(1)

