import gi
from gi.repository import Gst
from pipelines.BasePipeline import BasePipeline


class VideoPipeline(BasePipeline):
    def __init__(self, uri, image_queue):
        super().__init__(image_queue)
        self.uri = uri
        
        # Create GStreamer elements
        self.uridecodebin = Gst.ElementFactory.make("uridecodebin", "uridecodebin")
        self.queue = Gst.ElementFactory.make("queue", "queue")
        self.videoconvert = Gst.ElementFactory.make("qtivtransform", "qtivtransform")
        self.videoscale = Gst.ElementFactory.make("videoscale", "videoscale")
        self.capsfilter = Gst.ElementFactory.make("capsfilter", "capsfilter")
        self.appsink = Gst.ElementFactory.make("appsink", "appsink")

        if not all([self.uridecodebin, self.queue, self.videoconvert, self.videoscale, self.capsfilter, self.appsink]):
            print("Not all elements could be created")
            return

        print("Created all elements successfully")

    def configure_elements(self):
        self.uridecodebin.set_property("uri", self.uri)
        
        caps = Gst.Caps.from_string("video/x-raw,format=RGB,width=1280,height=720")
        self.capsfilter.set_property("caps", caps)

        self.appsink.set_property("emit-signals", True)
        self.appsink.set_property("sync", False)
        self.appsink.connect("new-sample", self.on_new_sample)

    def create(self):
        self.configure_elements()
        
        self.pipeline = Gst.Pipeline.new(self.uri)

        self.pipeline.add(self.uridecodebin)
        self.pipeline.add(self.queue)
        self.pipeline.add(self.videoconvert)
        self.pipeline.add(self.videoscale)
        self.pipeline.add(self.capsfilter)
        self.pipeline.add(self.appsink)

        self.uridecodebin.connect("pad-added", self.on_pad_added, self.queue)
        self.queue.link(self.videoconvert)
        self.videoconvert.link(self.videoscale)
        self.videoscale.link(self.capsfilter)
        self.capsfilter.link(self.appsink)

        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect("message", self.on_message)

        print("Elements linked successfully")

    def on_pad_added(self, uridecodebin, pad, queue):
        pad.link(queue.get_static_pad("sink"))
        print("Pad added and linked successfully")
