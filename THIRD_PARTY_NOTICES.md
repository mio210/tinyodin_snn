# Third-party notices

## tinyODIN HDL

Upstream: <https://github.com/ChFrenkel/tinyODIN>

Pinned commit: `18656534162a9de09b9954aea28fbfad7a7f8657`.

Files: `dut/rtl/aer_out.v`, `controller.v`, `fifo.v`, `lif_neuron.v`,
`neuron_core.v`, `scheduler.v`, `spi_slave.v`, `synaptic_core.v`, and `tinyODIN.v`.

Copyright (C) 2019-2022, Université catholique de Louvain (UCLouvain, Belgium),
University of Zürich (UZH, Switzerland), Katholieke Universiteit Leuven
(KU Leuven, Belgium), and Delft University of Technology (TU Delft, Netherlands).

Author: C. Frenkel, Delft University of Technology.

SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1

The upstream HDL is distributed under the Solderpad Hardware License v2.1;
see `dut/rtl/LICENSE` and the incorporated Apache text in
`dut/rtl/LICENSE.Apache-2.0`. Original rights, warranty exclusions and notices
remain applicable. This repository does not claim ownership of the tinyODIN
design or affiliation with its original authors.

The local HDL used by the benchmark matched the pinned upstream files after
removing comments and whitespace. The public export restores upstream opening
copyright/license/author/citation comments while retaining the benchmark's HDL
body. One upstream source and the upstream license used Windows-1252 text;
exported text is UTF-8. No HDL logic was changed by this export.

The upstream README asks users of the HDL to cite:

C. Frenkel, M. Lefebvre, J.-D. Legat and D. Bol,
"A 0.086-mm² 12.7-pJ/SOP 64k-Synapse 256-Neuron Online-Learning Digital Spiking
Neuromorphic Processor in 28-nm CMOS," IEEE Transactions on Biomedical Circuits
and Systems, vol. 13, no. 1, pp. 145-158, 2019.

The upstream documentation under `doc/` is not included in this export.

## Coverage adapter

The wrapper, harness, coverage metadata, interface specification and example
are separate benchmark additions. Upstream HDL notices apply to the upstream
files identified above. The adapter retains its existing licensing status;
this publication does not add a new license grant for those additions.
