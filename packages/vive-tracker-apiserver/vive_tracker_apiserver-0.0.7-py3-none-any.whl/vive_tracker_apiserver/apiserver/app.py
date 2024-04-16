import argparse
import io
import json
import logging
import os
import threading
import time
import os.path as osp
from typing import Optional, Dict, Union, Tuple, Any, List

import numpy as np
from vive_tracker_apiserver.common.functional import fix_vive_pose_matrix

from vive_tracker_apiserver.common import Config
from vive_tracker_apiserver.third_party import triad_openvr


class Application:
    __CONFIG_BUFFER_SIZE__ = 1024
    logger: logging.Logger
    option: Config
    cnt: int
    interval_s: float
    tracker_state_buffer: List[Tuple[dict, dict]]
    vr: Optional[triad_openvr.triad_openvr] = None
    poll_thread: Optional[threading.Thread]
    update_thread: Optional[threading.Thread]
    recording_thread: Optional[threading.Thread]
    recording_cancel_ev: threading.Event

    def __init__(self, cfg) -> None:
        if isinstance(cfg, Config):
            self.option = cfg
        elif isinstance(cfg, str):
            self.option = Config(cfg)
        elif isinstance(cfg, argparse.Namespace):
            self.option = Config(cfg.config)
        else:
            raise TypeError(
                "cfg must be Config, str, or argparse.Namespace"
            )
        if self.option.valid is False:
            raise ValueError("invalid config file")

        self.logger = logging.getLogger("apiserver.app")
        self.vr = triad_openvr.triad_openvr()

        self.logger.info('loading openvr components')
        [(time.sleep(1), print(".", end="")) for _ in range(3)]
        print('\n')
        self.logger.info("server is tarted!")

        self.vr_device_mapping = {x.get_serial(): index for index, x in self.vr.devices.items() if x.get_serial() in [x.uid for x in self.option.trackers]}
        self.cnt = 0
        self.interval_s = 1 / 250
        self.tracker_state_buffer = [
                                        (
                                            dict(
                                                index=-1,
                                                sys_ts_ns=0,
                                                uid="",
                                                valid=False
                                            ),
                                            dict()
                                        )
                                    ] * self.__CONFIG_BUFFER_SIZE__
        self.update_thread = None
        self.recording_thread = None
        self.recording_cancel_ev = threading.Event()

    def start_thread(self):

        def poll_thread(interval_s: float):
            while True:
                self.vr.poll_vr_events()
                time.sleep(interval_s)

        def update_vive_tracker_thread(interval_s):
            while True:
                start_t = time.time()
                meta = dict(
                    index=self.cnt,
                    sys_ts_ns=time.time_ns(),
                    uid="",
                    valid=True
                )
                try:
                    payload = {device_uid: fix_vive_pose_matrix(self.vr.devices[self.vr_device_mapping[device_uid]].get_pose_matrix()) for device_uid in self.vr_device_mapping.keys()}
                    meta['sys_ts_ns'] = int((time.time_ns() + meta['sys_ts_ns']) / 2)
                    meta['valid'] = all(map(lambda x: x is not None, payload.values()))
                    self.tracker_state_buffer[self.cnt % self.__CONFIG_BUFFER_SIZE__] = (
                        meta,
                        payload
                    )

                    self.cnt += 1
                    sleep_t = interval_s - (time.time() - start_t)
                    if sleep_t > 0:
                        time.sleep(sleep_t)
                except Exception as e:
                    self.logger.error(e)
                    self.logger.error('update thread is terminated')
                    time.sleep(1)

        self.poll_thread = threading.Thread(target=poll_thread, args=(30,), daemon=True)
        self.poll_thread.start()
        self.update_thread = threading.Thread(target=update_vive_tracker_thread, args=(self.interval_s,), daemon=True)
        self.update_thread.start()

    def get_single(self, device_uid: str, index=None) -> Tuple[Dict[str, Any], Optional[List[Union[int, float]]]]:
        index = self.cnt - 1 if index is None else index
        meta, data = self.tracker_state_buffer[index % self.__CONFIG_BUFFER_SIZE__]
        meta['uid'] = device_uid
        return meta, data[device_uid]

    def get_group(self, index=None) -> Tuple[Dict[str, Any], Optional[Dict[str, List[Union[int, float]]]]]:
        index = self.cnt - 1 if index is None else index
        return self.tracker_state_buffer[index % self.__CONFIG_BUFFER_SIZE__]

    def start_recording(self, tag: str) -> Optional[Exception]:
        if self.recording_thread is not None:
            return Exception("already recording")
        self.recording_cancel_ev.clear()

        def dump_buffer_thread(file: io.FileIO, cancel_ev: threading.Event):
            meta, payload = self.get_group()
            last_index = meta['index']

            while True:
                if cancel_ev.is_set():
                    file.flush()
                    break
                start_t = time.time()
                desired_index = last_index + 1
                meta, payload = self.get_group(index=desired_index)

                if not meta['valid'] or meta['index'] < desired_index:
                    sleep_t = self.interval_s - (time.time() - start_t)
                    if sleep_t > 0:
                        time.sleep(sleep_t)
                    continue

                else:
                    if meta['index'] > desired_index:
                        self.logger.warning('slow client operation detected')
                    last_index = meta['index']
                    file.write('[' + json.dumps(meta) + ',' + json.dumps({k: v.tolist() if v is not None else v for k,v in payload.items()}) + ']\n')

        if not osp.exists(self.option.data_path):
            os.makedirs(self.option.data_path)
        recording_file = open(osp.join(self.option.data_path, f'{tag}.jsonl'), 'w')
        self.recording_thread = threading.Thread(target=dump_buffer_thread, args=(recording_file, self.recording_cancel_ev), daemon=True)
        self.recording_thread.start()

        return None

    def stop_recording(self) -> Optional[Exception]:
        if self.recording_thread is None:
            return Exception("not recording")
        self.recording_cancel_ev.set()
        try:
            self.recording_thread.join(timeout=5)
            self.recording_thread = None
            return None
        except Exception as e:
            return e

    def shutdown(self):
        return None


if __name__ == '__main__':
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="./config.yaml")
    run_args = parser.parse_args(sys.argv[1:])

    logging.basicConfig(level=logging.INFO)

    app = Application(run_args)

    try:
        while True:
            print(app.get_group())

    except KeyboardInterrupt as e:
        app.shutdown()
