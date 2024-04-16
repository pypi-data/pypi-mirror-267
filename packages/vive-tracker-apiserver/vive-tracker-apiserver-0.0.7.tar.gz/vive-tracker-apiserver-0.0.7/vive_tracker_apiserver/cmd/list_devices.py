import pprint

from vive_tracker_apiserver.common import TrackerConfig
from vive_tracker_apiserver.third_party import triad_openvr as triad_openvr

def list_devices(args):
    v = triad_openvr.triad_openvr()
    trackers = [TrackerConfig(uid=x.get_serial(), name=name) for name, x in v.devices.items()]
    print("Detected Trackers:")
    print("-"*30)
    print("{:<20} {:<10}".format("UUID", "Name"))
    print("-"*30)
    for t in trackers:
        print("{:<20} {:<10}".format(t.uid, t.name))
    print("-"*30)