from vive_tracker_apiserver.third_party import triad_openvr as triad_openvr
import time
import sys

v = triad_openvr.triad_openvr()
v.print_discovered_objects()

if len(sys.argv) == 1:
    interval = 1/250
elif len(sys.argv) == 2:
    interval = 1/float(sys.argv[1])
else:
    print("Invalid number of arguments")
    interval = False

print(list(v.devices.keys()))
if interval:
    while(True):
        start = time.time()
        txt = ""

        res = v.devices["tracker_1"].get_pose_euler()
        if res is not None:
            for each in v.devices["tracker_1"].get_pose_euler():
                txt += "%.4f" % each
                txt += " "
        print("\r" + txt, end="")
        sleep_time = interval-(time.time()-start)
        if sleep_time>0:
            time.sleep(sleep_time)