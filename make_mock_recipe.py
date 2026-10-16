#!/usr/bin/env python3
"""Build a deterministic JSON fixture shaped like a useful LLM answer.

This fixture tests the LLM-to-Quest compiler and scheduling path; it is not
reported as evidence of a live model's reasoning quality.
"""
import json
import sys


def spi_steps(command, data):
    bits = [((command >> bit) & 1) for bit in range(19, -1, -1)]
    bits += [((data >> bit) & 1) for bit in range(19, -1, -1)]
    steps = [
        {"set": {"rst": 1, "sck": 0, "mosi": 0}, "repeat": 2},
        {"set": {"rst": 0, "sck": 0, "mosi": 0}, "repeat": 2},
    ]
    for bit in bits:
        steps.append({"set": {"rst": 0, "sck": 0, "mosi": bit},
                      "repeat": 1})
        steps.append({"set": {"rst": 0, "sck": 1, "mosi": bit},
                      "repeat": 1})
    steps.append({"set": {"rst": 0, "sck": 0, "mosi": 0}, "repeat": 2})
    return steps


def recipe(name, command, data, targets):
    return {"name": name, "targets": targets,
            "base": {"aerin_req": 0, "aerin_addr": 0, "aerout_ack": 0},
            "steps": spi_steps(command, data)}


payload = {"dut_name": "tinyodin_snn", "recipes": [
    recipe("cfg_gate_on", 0x40000, 1,
           ["config.enabled_closed"]),
    recipe("write_neuron_zero", 0x50000, 0x1234,
           ["opcode.neuron", "spi_event.program",
            "controller_state.write_neuron", "seq_spi_program.hit"]),
    recipe("write_synapse_zero", 0x60000, 0x00A5,
           ["opcode.synapse", "controller_state.write_synapse"]),
    recipe("read_neuron_zero", 0x90000, 0,
           ["spi_event.readback", "controller_state.read_neuron"]),
    recipe("read_synapse_zero", 0xA0000, 0,
           ["controller_state.read_synapse"]),
]}
with open(sys.argv[1], "w", encoding="utf-8") as handle:
    json.dump(payload, handle, separators=(",", ":"))
