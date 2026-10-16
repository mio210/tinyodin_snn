#!/usr/bin/env python3
import os
import subprocess

import run_verilator as rv


class VerilatorDut:
    def __init__(self):
        rv.ensure_built()
        self._p = subprocess.Popen(
            [rv.exe_path()], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            text=True, bufsize=1)
        self._header = self._p.stdout.readline().strip().split(",")
        self._last = {}

    @staticmethod
    def _line(action):
        return "%d %d %d %d %d %d" % (
            action.get("rst", 0) & 1, action.get("sck", 0) & 1,
            action.get("mosi", 0) & 1, action.get("aerin_req", 0) & 1,
            action.get("aerin_addr", 0) & 0x3FF,
            action.get("aerout_ack", 0) & 1)

    def step(self, action):
        self._p.stdin.write(self._line(action) + "\n")
        self._p.stdin.flush()
        line = self._p.stdout.readline()
        if not line:
            raise RuntimeError("tinyODIN Verilator process exited")
        values = [int(item) for item in line.strip().split(",")]
        self._last = rv.translate(dict(zip(self._header, values)))
        return self

    def reset(self):
        for _ in range(4):
            self.step({"rst": 1})
        for _ in range(4):
            self.step({"rst": 0})

    def read_signals(self):
        return self._last

    def close(self):
        process = getattr(self, "_p", None)
        if process is not None:
            try:
                process.stdin.close()
                process.wait(timeout=5)
            except Exception:
                process.kill()
            self._p = None

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass
