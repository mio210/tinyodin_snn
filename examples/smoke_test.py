#!/usr/bin/env python3
"""Build and exercise the independent tinyODIN coverage adapter, without an agent."""
import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from harness import TinyOdinHarness


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--steps", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()
    if args.steps < 1000:
        parser.error("--steps must be at least 1000")
    harness = TinyOdinHarness()
    cycles = 0
    previous = harness.reset()
    assert previous.shape == (52,) and not np.any(previous)

    def tick(action, repeat=1):
        nonlocal cycles, previous
        for _ in range(repeat):
            state, coverage, done, info = harness.step(action)
            assert state.shape == (52,) and state.dtype == np.float32
            assert np.all((state == 0) | (state == 1))
            assert np.all(state >= previous), "coverage decreased without reset"
            assert abs(coverage - float(state.sum()) / 52) < 1e-12
            assert abs(info["total_coverage"] - coverage * 100) < 1e-10
            previous = state.copy()
            cycles += 1

    def spi(command, data):
        for word in (command, data):
            for shift in range(19, -1, -1):
                bit = word >> shift & 1
                tick([0, 0, bit, 0, 0, 0])
                tick([0, 1, bit, 0, 0, 0])
        tick([0, 0, 0, 0, 0, 0], 6)

    try:
        tick([1, 0, 0, 0, 0, 0], 4)
        tick([0, 0, 0, 0, 0, 0], 8)
        spi(0x40000, 1)
        spi(0x40003, 255)
        spi(0x50000, 0x1234)
        spi(0x60000, 0x00A5)
        spi(0x90000, 0)
        spi(0xA0000, 0)
        for address in (0, 1, 255, 0x100, 0x200, 0x3FF):
            tick([0, 0, 0, 1, address, 1], 12)
            tick([0, 0, 0, 0, address, 0], 8)
        rng = np.random.default_rng(args.seed)
        while cycles < args.steps:
            tick([0, int(rng.integers(2)), int(rng.integers(2)),
                  int(rng.integers(2)), int(rng.integers(1024)), int(rng.integers(2))])
        covered = int(previous.sum())
        assert covered > 0
        print(json.dumps({"backend": "verilator", "steps": cycles, "seed": args.seed,
                          "covered_bins": covered, "total_bins": 52,
                          "coverage_pct": covered / 52 * 100,
                          "numpy_version": np.__version__,
                          "checks": "reset, binary shape, monotonic coverage and ratio passed"}))
        assert not np.any(harness.reset()), "reset did not clear coverage"
    finally:
        harness._dut.close()


if __name__ == "__main__":
    main()
