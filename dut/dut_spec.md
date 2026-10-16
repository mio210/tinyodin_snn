# tinyODIN SNN accelerator

This DUT is the open tinyODIN digital spiking-neural-network processor.  The
evaluation wrapper advances one `CLK` cycle for every action.  The controllable
pins are the asynchronous active-high reset, the SPI serial pins, the input AER
event link, and the output AER acknowledge.

## Action space

```text
action = [rst, sck, mosi, aerin_req, aerin_addr, aerout_ack]
```

| field | description | width |
|---|---:|---|
| `rst` | Asynchronous active-high reset. Normal operation uses 0. | 1 |
| `sck` | SPI clock driven by the test agent. | 1 |
| `mosi` | SPI input bit, sampled on each rising `sck` edge. | 1 |
| `aerin_req` | Input AER request, active high and synchronized to `CLK`. | 1 |
| `aerin_addr` | Input AER event. Bits `[7:0]` are neuron/address; bit 8 selects time-reference; bit 9 selects a virtual-synapse event. | 10 |
| `aerout_ack` | Acknowledge for an output AER request. | 1 |

## SPI transaction

SPI has no chip-select. A transaction is exactly 40 sampled MOSI bits, MSB
first. Keep each bit stable for a low and a high `sck` action, then return
`sck` low before the next bit. The first 20-bit word is the address/command and
the second 20-bit word is write data.

The first word is `{read, write, opcode[1:0], address[15:0]}`:

- `read=1` requests readback.
- `write=1` commits the second word.
- `opcode=0` accesses configuration registers.
- `opcode=1` accesses neuron memory.
- `opcode=2` accesses synapse memory.
- Configuration addresses 0, 1, 2, 3 program `gate_activity`, `open_loop`,
  `aer_source`, and `max_neuron` respectively.

A useful write therefore needs all 40 clocked bits; isolated `mosi` values do
nothing. Reset the SPI counter with `rst=1` before starting a fresh transaction.

Configuration writes update their latches directly and do **not** assert the
`spi_event.program` signal. That event is generated only by a completed write
whose opcode is neuron (`1`) or synapse (`2`). The controller accepts neuron
and synapse program/readback events only while `gate_activity=1`. Therefore a
recipe targeting the memory controller states must first write configuration
address 0 with data 1, allow at least three system clocks for synchronization,
and then issue the neuron/synapse frame without resetting in between. The
final falling edge that returns `sck` low commits a write transaction.

## AER handshake

Hold `aerin_req=1` for at least four system cycles so the two-stage synchronizer
sees it. Keep `aerin_addr` stable until `AERIN_ACK=1`, then lower the request.
Neuron events use bit 8=0 and bit 9=0; time-reference events use bit 8=1;
virtual events use bit 9=1. Output events use a four-phase handshake: when
`AEROUT_REQ=1`, raise `aerout_ack`, wait for request to fall, then lower ack.

The scheduler FIFO is only four entries deep, so bursts of input virtual or
neuron events can reach the full state. Protocol ordering and multi-cycle
sequences are essential for the difficult coverage bins.
