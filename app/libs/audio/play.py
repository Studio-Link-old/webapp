# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +--------------------------------------------------------------------------+
# |   _____ __            ___          ______                            __  |
# |  / ___// /___  ______/ (_)___     / ____/___  ____  ____  ___  _____/ /_ |
# |  \__ \/ __/ / / / __  / / __ \   / /   / __ \/ __ \/ __ \/ _ \/ ___/ __/ |
# | ___/ / /_/ /_/ / /_/ / / /_/ /  / /___/ /_/ / / / / / / /  __/ /__/ /_   |
# |/____/\__/\__,_/\__,_/_/\____/   \____/\____/_/ /_/_/ /_/\___/\___/\__/   |
# |Copyright Sebastian Reimers 2013 studio-connect.de                        |
# |License: BSD-2-Clause (see LICENSE File)                                  |
# +--------------------------------------------------------------------------+

import gi
import os
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, GLib
GObject.threads_init()
Gst.init(None)

Gst.debug_set_active(True)
Gst.debug_set_default_threshold(3)

_basedir = os.path.abspath(os.path.dirname(__file__))

class Play:
    def __init__(self, audio_device='hw:0'):
        self.pipeline = Gst.Pipeline()


        # Location
        self.filesrc = Gst.ElementFactory.make('filesrc', None)
        self.filesrc.set_property('location', os.path.join(_basedir, 'speech_orig.wav'))

        # wavparse
        self.wavparse = Gst.ElementFactory.make('wavparse', None)

        # audioconvert
        self.audioconvert = Gst.ElementFactory.make('audioconvert', None)
    
        # alsasink
        self.alsasink = Gst.ElementFactory.make('alsasink', None)
        self.alsasink.set_property('device', audio_device)

        # Pipe Adding/Linking
        self.pipeline.add(self.filesrc)
        self.pipeline.add(self.wavparse)
        self.pipeline.add(self.audioconvert)
        self.pipeline.add(self.alsasink)
        self.filesrc.link(self.wavparse)
        self.wavparse.link(self.audioconvert)
        self.audioconvert.link(self.alsasink)

        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message::eos', self.on_eos)
        self.bus.connect("message", self.on_message)

    def run(self):
        self.pipeline.set_state(Gst.State.PLAYING)

    def loop(self):
        try:
            self.loop = GObject.MainLoop()
            self.loop.run()
        except Exception, e:
           print("Exception encountered - %s" % e)
           self.pipeline.set_state(Gst.State.NULL)

    def on_eos(self, bus, message):
        self.pipeline.set_state(Gst.State.NULL)
        self.loop.quit()

    def on_message(self, bus, msg):
        pass

if __name__ == "__main__":
    player = Play()
    player.run()
    player.loop()
