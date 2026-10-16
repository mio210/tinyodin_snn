#!/usr/bin/env python3
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))


def exe_path():
    return os.path.join(HERE, "obj_dir", "Vtinyodin_cov_top")


def ensure_built():
    if os.path.exists(exe_path()):
        return
    result = subprocess.run(
        ["bash", os.path.join(HERE, "build.sh")],
        text=True, capture_output=True)
    if result.returncode or not os.path.exists(exe_path()):
        raise RuntimeError("tinyODIN Verilator build failed:\n%s\n%s" %
                           (result.stdout, result.stderr))


def translate(sig):
    return {
        "rst": sig.get("rst", 0), "sck": sig.get("sck", 0),
        "mosi": sig.get("mosi", 0), "spi_cnt": sig.get("spi_cnt", 0),
        "opcode": sig.get("opcode", 0), "prog": sig.get("prog", 0),
        "read": sig.get("read", 0), "gate": sig.get("gate", 0),
        "open": sig.get("open", 0), "aer_source": sig.get("aer_source", 0),
        "max_neur": sig.get("max_neur", 0),
        "aerin_type": (sig.get("aerin_addr", 0) >> 8) & 3,
        "aerin_low": sig.get("aerin_addr", 0) & 255,
        "aerin_req": sig.get("aerin_req", 0),
        "aerin_ack": sig.get("aerin_ack", 0),
        "aerout_req": sig.get("aerout_req", 0),
        "aerout_ack": sig.get("aerout_ack", 0),
        "aerout_addr": sig.get("aerout_addr", 0),
        "sched_full": sig.get("sched_full", 0),
        "ctrl_state": sig.get("ctrl_state", 0),
        "seq_reset_release": sig.get("sq_reset", 0),
        "seq_spi_program": sig.get("sq_spi", 0),
        "seq_aer_handshake": sig.get("sq_aer", 0),
        "seq_spi_then_aer": sig.get("sq_spi_aer", 0),
        "seq_req_hold": sig.get("sq_hold", 0),
    }
