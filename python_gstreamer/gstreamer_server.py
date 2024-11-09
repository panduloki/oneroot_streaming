import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

def main():
    # Initialize GStreamer
    Gst.init(None)

    # Create the pipeline for the RTSP server
    pipeline = Gst.Pipeline.new("rtsp-server")
    print("Created GStreamer pipeline")

    # Step 1: Create the source element to capture video from the USB camera
    try:
        source = Gst.ElementFactory.make("v4l2src", "source")
        if not source:
            raise Exception("Failed to create v4l2src element")
        source.set_property("device", "/dev/video0")  # Adjust the device path if needed
        print("Configured source element to capture from /dev/video0")
    except Exception as e:
        print(f"Error creating source element: {e}")
        return

    # Step 2: Convert a video format to a compatible format for encoding
    try:
        videoconvert = Gst.ElementFactory.make("videoconvert", "videoconvert")
        if not videoconvert:
            raise Exception("Failed to create videoconvert element")
        print("Video convert element created")
    except Exception as e:
        print(f"Error creating videoconvert element: {e}")
        return

    # Step 3: Encode video in H.264 format
    try:
        x264enc = Gst.ElementFactory.make("x264enc", "x264enc")
        if not x264enc:
            raise Exception("Failed to create x264enc element")
        x264enc.set_property("bitrate", 1000000)  # Adjust bitrate as needed
        print("Video encoder configured with bitrate 1000000")
    except Exception as e:
        print(f"Error creating x264enc element: {e}")
        return

    # Step 4: RTP packetizer for H.264 stream
    try:
        rtppay = Gst.ElementFactory.make("rtph264pay", "rtppay")
        if not rtppay:
            raise Exception("Failed to create rtph264pay element")
        print("RTP H.264 packetizer element created")
    except Exception as e:
        print(f"Error creating rtph264pay element: {e}")
        return

    # Step 5: RTSP server to serve the RTP stream
    try:
        rtspserver = Gst.ElementFactory.make("rtspserver", "rtspserver")
        if not rtspserver:
            raise Exception("Failed to create rtspserver element")
        rtspserver.set_property("service", "8554")
        print("RTSP server configured on port 8554")
    except Exception as e:
        print(f"Error creating rtspserver element: {e}")
        return

    # Add elements to the pipeline and link them
    pipeline.add(source)
    pipeline.add(videoconvert)
    pipeline.add(x264enc)
    pipeline.add(rtppay)
    pipeline.add(rtspserver)
    print("Added elements to the pipeline")

    # Try linking the pipeline elements
    try:
        source.link(videoconvert)
        videoconvert.link(x264enc)
        x264enc.link(rtppay)
        rtppay.link(rtspserver)
        print("Pipeline elements linked successfully")
    except Exception as e:
        print(f"Error linking pipeline elements: {e}")
        return

    # Start the pipeline
    ret = pipeline.set_state(Gst.State.PLAYING)
    if ret == Gst.StateChangeReturn.FAILURE:
        print("Failed to start pipeline")
        return
    else:
        print("Pipeline started, RTSP server running on port 8554")

    # Run the main loop to keep the pipeline running
    try:
        loop = GLib.MainLoop()
        loop.run()
    except KeyboardInterrupt:
        print("Shutting down RTSP server")
    finally:
        # Ensure the pipeline is properly cleaned up
        pipeline.set_state(Gst.State.NULL)
        print("Pipeline stopped and cleaned up")

if __name__ == "__main__":
    main()
