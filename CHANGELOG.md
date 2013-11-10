# Changelog

## v13.11-alpha (xx.11.2013)
Bootstrap3, security and bugfix release

### Webapp

#### Features

- Update template to Bootstrap 3
- add ip6tables ruleset
- Optimize shutdown/reboot handling
- HTTP basic access authentication
- Capture Mixer
- User Password Change

#### Bugfixes

- Call Unhandled Exception (#5)
- Firefox glyphicons bug (#1)
- Exchange audio caps between peers (#2)
- Receiver settings not implemented (jitter, bitrate) (#11)

### Image

- Mainline Linux Kernel 3.12
- Enable IPv4 autoconfiguration (RFC 3927)
- Unique hostname (based on mac hash)
- Update function (SSH only at the moment)


## v0.2.0-dev (04.10.2013)
Full integrated Gstreamer Opus Webinterface with IPv6 peering.

- Replace Debian Wheezy with Archlinux (newer packages etc.)
- Fix Shure X2u Sound Quality (only 32kHz on RaspberryPi)
- Simple Peer CRUD functions
- Peering (invite and status) REST API
- Unittests
- Audio Playbacktest
- Shutdown and Reboot
- Add settings menu (select audio device)


## v0.1.0-dev (29.06.2013)
First prototype release.

- Flask Webinterface
- Alsa javascript equalizer
- Basic i18n support
- Aiccu support
