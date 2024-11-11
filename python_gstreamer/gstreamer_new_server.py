import gi
import socket  # Import socket module here

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

if __name__ == '__main__':
    try:
        # Start the RTSP server and run the GObject main loop to handle requests
        server = RtspServer()
        print("Starting GObject Main Loop...")
        loop = GObject.MainLoop()
        loop.run()
    except Exception as e:
        print("An error occurred:", e)
        print("Exiting...")

