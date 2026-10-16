#!/bin/bash
set -e
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DUT="${HERE}/../dut"
OBJ="${HERE}/obj_dir"
rm -rf "${OBJ}"
verilator --cc --exe --public --top-module tinyodin_cov_top \
  -Mdir "${OBJ}" -Wno-fatal -Wno-WIDTH -Wno-UNUSEDSIGNAL \
  -Wno-UNUSEDPARAM -Wno-LATCH -Wno-CASEINCOMPLETE \
  "${HERE}/sim_main.cpp" "${DUT}/tinyodin_cov_top.v" \
  "${DUT}/rtl/aer_out.v" "${DUT}/rtl/controller.v" \
  "${DUT}/rtl/fifo.v" "${DUT}/rtl/lif_neuron.v" \
  "${DUT}/rtl/neuron_core.v" "${DUT}/rtl/scheduler.v" \
  "${DUT}/rtl/spi_slave.v" "${DUT}/rtl/synaptic_core.v" \
  "${DUT}/rtl/tinyODIN.v"
make -C "${OBJ}" -j"$(nproc)" -f Vtinyodin_cov_top.mk Vtinyodin_cov_top
