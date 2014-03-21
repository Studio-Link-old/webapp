# Changelog

## v14.3.0-alpha (xx.03.2014)

### Webapp

#### Features

- Update template to Bootstrap 3.1.1
- add ip6tables ruleset
- Optimize shutdown/reboot handling
- HTTP basic access authentication
- Capture Mixer
- User Password Change
- Baresip 0.4.10 (replace gstreamer/openob)
- New Peer concept (based on SIP User Agents)

#### Bugfixes

- Firefox glyphicons bug (#1)
- Dashboard javascript title overwrite

### Image

- Mainline Linux Kernel 3.13
- Opus 1.1
- Enable IPv4 autoconfiguration (RFC 3927)
- Unique hostname (based on mac)
- Update function (SSH only at the moment)
- Cleanup old systemd scripts


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
