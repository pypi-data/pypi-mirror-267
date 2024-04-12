import ray

import numpy as np


@ray.remote(num_cpus=0.1, resources={"worker1": 1e-4})
class Noop12:
    def __init__(self, payload: str):
        self.payload = payload

    def start(self, spice_loc_map: np.ndarray, spice_value_map: np.ndarray, order_map: dict):
        pass

@ray.remote(num_cpus=0.1, resources={"worker2": 1e-4})
class Noop34:
    def __init__(self, payload: str):
        self.payload = payload

    def start(self, spice_loc_map: np.ndarray, spice_value_map: np.ndarray, order_map: dict):
        pass

