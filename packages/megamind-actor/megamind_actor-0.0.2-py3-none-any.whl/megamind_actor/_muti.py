import socket
from contextlib import closing
from typing import Tuple

import ray

from ._job import JobConf


class MegamindMulti:
    def __init__(self, node_rank: int, config: JobConf) -> None:
        self._node_rank = node_rank
        self._config = config
        self._local_node_id = ray.util.get_node_ip_address()
        self._local_gpu_ids = ray.get_gpu_ids()

    @property
    def config(self) -> JobConf:
        return self._config

    def _is_master(self) -> bool:
        return self._node_rank == 0

    def get_node_info(self) -> Tuple[str, int, list]:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.bind(("", 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            port = s.getsockname()[1]
            return self._local_node_id, port, self._local_gpu_ids

    def launch(self, **kwargs):
        print("this is a test")

