import gi
from gi.repository import Gst
from pipelines.BasePipeline import BasePipeline


class WebcamPipeline(BasePipeline):
    def __init__(self, device, image_queue):
        super().__init__(image_queue)
        self.device = device
        
        # Create GStreamer elements
        self.v4l2src = Gst.ElementFactory.make("v4l2src", "v4l2src")
        self.queue = Gst.ElementFactory.make("queue", "queue")
        self.videoconvert = Gst.ElementFactory.make("qtivtransform", "qtivtransform")
        self.videoscale = Gst.ElementFactory.make("videoscale", "videoscale")
        self.capsfilter = Gst.ElementFactory.make("capsfilter", "capsfilter")
        self.appsink = Gst.ElementFactory.make("appsink", "appsink")

        if not all([self.v4l2src, self.queue, self.videoconvert, self.videoscale, self.capsfilter, self.appsink]):
            print("Not all elements could be created")
            return

        print("Created all elements successfully")

    def configure_elements(self):
        self.v4l2src.set_property("device", self.device)
        
        caps = Gst.Caps.from_string("video/x-raw,format=RGB,width=1920,height=1080")
        self.capsfilter.set_property("caps", caps)

        self.appsink.set_property("emit-signals", True)
        self.appsink.set_property("sync", False)
        self.appsink.connect("new-sample", self.on_new_sample)

    def create(self):
        self.configure_elements()
        
        self.pipeline = Gst.Pipeline.new("webcam-pipeline")

        self.pipeline.add(self.v4l2src)
        self.pipeline.add(self.queue)
        self.pipeline.add(self.videoconvert)
        self.pipeline.add(self.videoscale)
        self.pipeline.add(self.capsfilter)
        self.pipeline.add(self.appsink)

        self.v4l2src.link(self.queue)
        self.queue.link(self.videoconvert)
        self.videoconvert.link(self.videoscale)
        self.videoscale.link(self.capsfilter)
        self.capsfilter.link(self.appsink)

        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect("message", self.on_message)

        print(f"Webcam pipeline created for {self.device}")
