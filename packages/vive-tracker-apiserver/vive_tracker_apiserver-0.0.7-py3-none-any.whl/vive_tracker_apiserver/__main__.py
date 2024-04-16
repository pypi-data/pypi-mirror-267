import argparse
import sys

import vive_tracker_apiserver.apiserver as apiserver
import vive_tracker_apiserver.cmd as cmd

parser = argparse.ArgumentParser()

args = sys.argv[1:]
if len(args) == 0:
    exit(print("No arguments provided"))
if args[0] == "configure":
    exit(cmd.configure(args[1:]))
elif args[0] == "list":
    exit(cmd.list_devices(args[1:]))
elif args[0] == "serve":
    exit(apiserver.serve(args[1:]))
elif args[0] == "test.server":
    exit(cmd.test_server())
elif args[0] == "test.visualize":
    exit(cmd.test_visualize())
else:
    print("Unknown command {}, available commands are:".format(args[0]))
    print("-"*60)
    print("{:<20} {:<40}".format("Name", "Description"))
    print("-"*60)
    print("{:<20} {:<40}".format("configure", "Generate configuration"))
    print("{:<20} {:<40}".format("list", "List trackers"))
    print("{:<20} {:<40}".format("serve", "Launch the server"))
    print("{:<20} {:<40}".format("test.server", "Test server connection"))
    print("{:<20} {:<40}".format("test.visualize", "Test visualization with Open3d"))
    print("-"*60)