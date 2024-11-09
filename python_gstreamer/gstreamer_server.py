import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

def main():
    Gst.init(None)

    # Create the pipeline
    pipeline = Gst.Pipeline.new("rtsp-server")

    # Source: Capture video from the USB camera
    source = Gst.ElementFactory.make("v4l2src")
    source.set_property("device", "/dev/video0")  # Adjust device path if needed

    # Convert video format
    videoconvert = Gst.ElementFactory.make("videoconvert")

    # Encode video in H.264 format
    x264enc = Gst.ElementFactory.make("x264enc")
    x264enc.set_property("bitrate", 1000000)  # Adjust bitrate as needed

    # RTP packetizer
    rtppay = Gst.ElementFactory.make("rtph264pay")

    # RTSP server
    rtspserver = Gst.ElementFactory.make("rtspserver")
    rtspserver.set_property("service", "8554")

    # Link elements in the pipeline
    pipeline.add(source)
    pipeline.add(videoconvert)
    pipeline.add(x264enc)
    pipeline.add(rtppay)
    pipeline.add(rtspserver)

    try:
        source.link(videoconvert)
        videoconvert.link(x264enc)
        x264enc.link(rtppay)
        rtppay.link(rtspserver)
    except Exception as e:
        print(f"Error linking pipeline elements: {e}")
        return

    # Start the pipeline
    ret = pipeline.set_state(Gst.State.PLAYING)
    if ret == Gst.StateChangeReturn.FAILURE:
        print("Failed to start pipeline")
        return

    print("RTSP server started on port 8554")

    # Keep the pipeline running
    loop = Gst.MainLoop()
    loop.run()

if __name__ == "__main__":
    main()