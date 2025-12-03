import gi
from gi.repository import Gst, GLib
import numpy as np


class BasePipeline:
    def __init__(self, image_queue):
        self.pipeline = None
        self.bus = None
        self.loop = None
        self.image_queue = image_queue
        self.appsink = None

    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            print("------------EOS--------------------------")
            self.reconnect()
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print(f"Error: {err}, {debug}")
        elif t == Gst.MessageType.WARNING:
            warn, debug = message.parse_warning()
            print(f"Warning: {warn}, {debug}")

    def reconnect(self):
        print("Reconnecting pipeline...")
        self.pipeline.set_state(Gst.State.NULL)
        self.pipeline.set_state(Gst.State.READY)
        self.pipeline.set_state(Gst.State.PLAYING)

    def start(self):
        if self.pipeline is not None:
            self.pipeline.set_state(Gst.State.PLAYING)
            self.loop = GLib.MainLoop()
            self.loop.run()

    def destroy(self):
        if self.pipeline is not None:
            self.pipeline.set_state(Gst.State.NULL)
            print("Pipeline set to NULL (stopped)")

    def on_new_sample(self, appsink, data=None):
        sample = self.appsink.emit("pull-sample")
        if isinstance(sample, Gst.Sample):
            buffer = sample.get_buffer()
            caps = sample.get_caps()
            width = caps.get_structure(0).get_value("width")
            height = caps.get_structure(0).get_value("height")
            channels = 3

            buffer_size = buffer.get_size()
            np_array = np.ndarray(shape=(height, width, channels),
                                  dtype=np.uint8,
                                  buffer=buffer.extract_dup(0, buffer_size))

            np_array = np.copy(np_array)
            
            if self.image_queue.full():
                self.image_queue.get()

            self.image_queue.put(np_array)

            return Gst.FlowReturn.OK
        else:
            print("Failed to get sample")
            return Gst.FlowReturn.ERROR
