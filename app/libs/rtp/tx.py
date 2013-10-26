# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright (c) 2012, James Harrison https://github.com/JamesHarrison/openob

import sys
import time
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

#Gst.debug_set_active(True)
#Gst.debug_set_default_threshold(3)

GObject.threads_init()

Gst.init(None)


class RTPtransmitter:
    def __init__(self, audio_device='hw:0', base_port=3000, ipv6=True, bitrate=64, receiver_address='::', opus_options={'audio': True, 'bandwidth': -1000, 'frame-size': 20, 'complexity': 3, 'constrained-vbr': True, 'inband-fec': True, 'packet-loss-percentage': 1, 'dtx': False}):
        """Sets up a new RTP transmitter"""

        self.pipeline = Gst.Pipeline()
        self.started = False

        self.source = Gst.ElementFactory.make('alsasrc', None)
        self.source.set_property('device', audio_device)
        self.source.set_property('buffer-time', 25000)
        self.source.set_property('latency-time', 5000)

        self.caps = 'None'

        # Audio conversion and resampling
        self.audioconvert = Gst.ElementFactory.make("audioconvert", None)
        self.audioresample = Gst.ElementFactory.make("audioresample", None)
        self.audioresample.set_property('quality', 9) # SRC

        self.encoder = Gst.ElementFactory.make("opusenc", "encoder")
        self.encoder.set_property('bitrate', bitrate*1000)
        for key, value in opus_options.iteritems():
            self.encoder.set_property(key, value)
        self.payloader = Gst.ElementFactory.make("rtpopuspay", "payloader")

        # Now the RTP bits
        # We'll send audio out on this
        self.udpsink_rtpout = Gst.ElementFactory.make("udpsink", "udpsink_rtp")
        self.udpsink_rtpout.set_property('host', receiver_address)
        self.udpsink_rtpout.set_property('port', base_port)
        # And send our control packets out on this
        self.udpsink_rtcpout = Gst.ElementFactory.make("udpsink", "udpsink_rtcp")
        self.udpsink_rtcpout.set_property('host', receiver_address)
        self.udpsink_rtcpout.set_property('port', base_port+1)
        self.udpsink_rtcpout.set_property('sync', False)
        self.udpsink_rtcpout.set_property('async', False)

        # And the receiver will send us RTCP Sender Reports on this
        self.udpsrc_rtcpin = Gst.ElementFactory.make("udpsrc", "udpsrc_rtcp")
        self.udpsrc_rtcpin.set_property('port', base_port+2)
        if(ipv6):
             self.udpsrc_rtcpin.set_property('multicast-group', "::")
        # (but we'll ignore them/operate fine without them because we assume we're 
        # stuck behind a firewall)
        # Our RTP manager
        self.rtpbin = Gst.ElementFactory.make("rtpbin",None)

        # Add to the pipeline
        self.pipeline.add(self.rtpbin)
        self.pipeline.add(self.source)
        self.pipeline.add(self.audioconvert)
        self.pipeline.add(self.audioresample)
        self.pipeline.add(self.encoder)
        self.pipeline.add(self.payloader)
        self.pipeline.add(self.udpsink_rtpout)
        self.pipeline.add(self.udpsink_rtcpout)
        self.pipeline.add(self.udpsrc_rtcpin)


        self.source.link(self.audioresample)
        self.audioresample.link(self.audioconvert)
        self.audioconvert.link(self.encoder)
        self.encoder.link(self.payloader)

        # And now the RTP bits
        self.payloader.link_pads('src', self.rtpbin, 'send_rtp_sink_0')
        self.rtpbin.link_pads('send_rtp_src_0', self.udpsink_rtpout, 'sink')
        self.rtpbin.link_pads('send_rtcp_src_0', self.udpsink_rtcpout, 'sink')
        self.udpsrc_rtcpin.link_pads('src', self.rtpbin, 'recv_rtcp_sink_0')

        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message::eos', self.on_eos)
        self.bus.connect("message", self.on_message)

    def run(self):
        self.udpsink_rtcpout.set_locked_state(Gst.State.PLAYING)
        self.pipeline.set_state(Gst.State.PLAYING)
        while self.caps == 'None':
            self.pipeline.get_state(0)
            time.sleep(2)  # Bugfix wait for caps
            print(" -- Waiting for caps - if you get this a lot, you probably can't access the requested audio device.")
            self.caps = self.udpsink_rtpout.get_static_pad('sink').get_property('caps').to_string()
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
    transmitter = RTPtransmitter(audio_device="hw:0", ipv6=False, receiver_address='127.0.0.1')
    transmitter.run()
    print("   - Caps:          %s" % transmitter.caps)
    while True:
        Gst.Bus.poll(transmitter.pipeline.get_bus(), 0, 1)
        time.sleep(1)

