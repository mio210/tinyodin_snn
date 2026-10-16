#!/usr/bin/env python3
import importlib.util
import os
import sys
from typing import Dict, Optional

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


class TinyOdinHarness:
    DIMS = 6

    def __init__(self, secrets: Optional[Dict] = None,
                 backend: str = "verilator"):
        if backend != "verilator":
            raise ValueError("tinyodin_snn supports only verilator")
        sys.path.insert(0, os.path.join(HERE, "verilator_harness"))
        import verilator_dut
        self._dut = verilator_dut.VerilatorDut()
        spec = importlib.util.spec_from_file_location(
            "tinyodin_cov", os.path.join(HERE, "coverage_simulator.py"))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self._cs = module.CoverageSimulator(
            os.path.join(HERE, "dut", "coverage_meta.json"))
        self.backend = backend
        self.reset()

    def reset(self):
        self._dut.reset()
        self._cs.reset()
        return self._state()

    def _state(self):
        return np.asarray(self._cs.get_bin_vector(), dtype=np.float32)

    @property
    def total_bins(self):
        return self._cs.total_bins

    @property
    def coverage(self):
        return self._cs.coverage

    def step(self, stimulus):
        values = [int(x) for x in np.asarray(
            stimulus, dtype=np.float32).reshape(-1)]
        values += [0] * max(0, self.DIMS - len(values))
        self._dut.step({
            "rst": values[0] & 1,
            "sck": values[1] & 1,
            "mosi": values[2] & 1,
            "aerin_req": values[3] & 1,
            "aerin_addr": values[4] & 0x3FF,
            "aerout_ack": values[5] & 1,
        })
        self._cs.step(self._dut.read_signals())
        state = self._state()
        return state, float(np.sum(state)) / self.total_bins, False, {
            "total_coverage": self._cs.coverage * 100.0}
