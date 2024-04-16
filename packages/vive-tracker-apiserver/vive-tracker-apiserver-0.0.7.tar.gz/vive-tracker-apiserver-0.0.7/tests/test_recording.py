import time
from vive_tracker_apiserver.client import Client

def get_description(data):
    return str([f'id:{item.meta.uid} x: {item.pos_x:.2f} y: {item.pos_y:.2f} z: {item.pos_z:.2f}' for item in data.payload])

def test():
    endpoint = "localhost:8080"

    c = Client(endpoint)

    response = c.start_recording("test" + str(time.time()))
    print("StartRecording client received: " + str(response))

    time.sleep(20)

    response = c.stop_recording()
    print("StopRecording client received: " + str(response))

if __name__ == '__main__':
    test()