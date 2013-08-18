import sys
import time
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

#Gst.debug_set_active(True)
#Gst.debug_set_default_threshold(3)

GObject.threads_init()
Gst.init(None)


class RTPreceiver:
    def __init__(self, caps='', audio_device='hw:0', base_port=3000,
                 ipv6=True,  bitrate=96, jitter_buffer=150):
        """Sets up a new RTP receiver"""

        self.pipeline = Gst.Pipeline()
        self.started = False

        self.sink = Gst.ElementFactory.make("alsasink", None)
        self.sink.set_property('device', audio_device)

        self.audioconvert = Gst.ElementFactory.make("audioconvert", None)
        self.audioresample = Gst.ElementFactory.make("audioresample", None)
        self.audioresample.set_property('quality', 9)

        self.decoder = Gst.ElementFactory.make("opusdec", "decoder")
        self.decoder.set_property('use-inband-fec', True)  # FEC
        self.decoder.set_property('plc', True)  # Packet loss concealment
        self.depayloader = Gst.ElementFactory.make("rtpopusdepay",
                                                   "depayloader")

        self.rtpbin = Gst.ElementFactory.make('rtpbin', None)
        self.rtpbin.set_property('latency', jitter_buffer)
        self.rtpbin.set_property('autoremove', True)
        self.rtpbin.set_property('do-lost', True)

        self.udpsrc_rtpin = Gst.ElementFactory.make('udpsrc', None)
        self.udpsrc_rtpin.set_property('port', base_port)
        caps = caps.replace('\\', '')
        udpsrc_caps = Gst.caps_from_string(caps)
        self.udpsrc_rtpin.set_property('caps', udpsrc_caps)
        self.udpsrc_rtpin.set_property('timeout', 5000000)

        # Where our RTCP control messages come in
        self.udpsrc_rtcpin = Gst.ElementFactory.make('udpsrc', None)
        self.udpsrc_rtcpin.set_property('port', base_port+1)
        # And where we'll send RTCP Sender Reports
        # (a black hole - we assume we can't contact the sender,
        # and this is optional)
        self.udpsink_rtcpout = Gst.ElementFactory.make('udpsink', None)
        self.udpsink_rtcpout.set_property('port', base_port+2)
        if (ipv6):
            self.udpsrc_rtpin.set_property('multicast-group', "::")
            self.udpsrc_rtcpin.set_property('multicast-group', "::")
            self.udpsink_rtcpout.set_property('host', "::")
        else:
            self.udpsink_rtcpout.set_property('host', "0.0.0.0")

        # And now we've got it all set up we need to add the elements
        self.pipeline.add(self.audioresample)
        self.pipeline.add(self.audioconvert)
        self.pipeline.add(self.sink)
        self.pipeline.add(self.depayloader)
        self.pipeline.add(self.rtpbin)
        self.pipeline.add(self.udpsrc_rtpin)
        self.pipeline.add(self.udpsrc_rtcpin)
        self.pipeline.add(self.udpsink_rtcpout)
        self.pipeline.add(self.decoder)

        self.depayloader.link(self.decoder)
        self.decoder.link(self.audioconvert)
        self.audioconvert.link(self.audioresample)
        self.audioresample.link(self.sink)

        # Now the RTP pads
        self.udpsrc_rtpin.link_pads('src', self.rtpbin, 'recv_rtp_sink_0')
        self.udpsrc_rtcpin.link_pads('src', self.rtpbin, 'recv_rtcp_sink_0')
        # RTCP SRs
        self.rtpbin.link_pads('send_rtcp_src_0', self.udpsink_rtcpout, 'sink')

        # Attach callbacks for dynamic pads (RTP output) and busses
        self.rtpbin.connect('pad-added', self.rtpbin_pad_added)

        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message::eos', self.on_eos)
        self.bus.connect("message", self.on_message)

    # Our RTPbin won't give us an audio pad till it receives,
    # so we need to attach it here
    def rtpbin_pad_added(self, obj, pad):
        # Unlink first.
        self.rtpbin.unlink(self.depayloader)
        # Relink
        self.rtpbin.link(self.depayloader)

    def run(self):
        self.pipeline.set_state(Gst.State.PLAYING)
        self.started = True

    def on_eos(self, bus, message):
        self.pipeline.set_state(Gst.State.NULL)
        print "STOPPED"

    def on_message(self, bus, msg):
        if (msg.type == msg.type.ERROR):
            print msg.parse_error()
        if (msg.type == msg.type.INFO):
            print msg.parse_info()
        if (msg.type == msg.type.WARNING):
            print msg.parse_warning()

if __name__ == "__main__":
    caps = "application/x-rtp,media=(string)audio,clock-rate=(int)48000,encoding-name=(string)X-GST-OPUS-DRAFT-SPITTKA-00"
    receiver = RTPreceiver(caps=caps, audio_device='hw:2', ipv6=False)
    receiver.run()
    while True:
        Gst.Bus.poll(receiver.pipeline.get_bus(), 0, 1)
        time.sleep(1)
#    loop = GLib.MainLoop()
#    loop.run()
