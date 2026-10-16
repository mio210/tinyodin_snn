# tinyODIN SNN functional coverage benchmark

独立的 tinyODIN SNN 功能覆盖评测题包：Verilog RTL、Verilator 仿真桥、
Python harness、接口规格和 **52 个有序覆盖 bin**。每条 action 推进一个真实 RTL
系统时钟周期，不依赖外部求解器、LLM 服务或其他私有项目。

tinyODIN 原始设计来自 [ChFrenkel/tinyODIN](https://github.com/ChFrenkel/tinyODIN)。
本仓库增加覆盖观察 wrapper 和评测接口，不是原作者的官方发布。
九个 RTL 文件已与固定上游版本核对，忽略注释和空白后的代码相同；公开导出时
恢复了上游版权、许可和作者注释。版本及逐文件 SHA256 见
[SOURCE_PROVENANCE.json](SOURCE_PROVENANCE.json)。

## 快速运行

Linux / WSL 下安装 Python 3、NumPy、Verilator、GNU Make 和 C++ 编译器。例如：

```bash
sudo apt-get update
sudo apt-get install -y python3 python3-numpy verilator make g++
git clone https://github.com/mio210/tinyodin_snn.git
cd tinyodin_snn
python3 examples/smoke_test.py --steps 2000 --seed 1
```

如果使用独立 Python 虚拟环境，也可以通过 `python3 -m pip install -r requirements.txt`
安装 Python 依赖。第一次运行会自动编译 Verilator 模型。结果以 JSON 输出实际周期、
命中数和覆盖率；这个确定性运行检查不是智能搜索算法的成绩。

## 接口

```python
from harness import TinyOdinHarness

harness = TinyOdinHarness(backend="verilator")
state = harness.reset()  # float32 ndarray, shape (52,)
state, coverage, done, info = harness.step([0, 0, 0, 0, 0, 0])
```

Action 顺序为 `[rst, sck, mosi, aerin_req, aerin_addr, aerout_ack]`。
具体位宽、SPI 帧和 AER 握手见 [dut/dut_spec.md](dut/dut_spec.md)。
`coverage` 是 0～1 的累计覆盖比例，`info["total_coverage"]` 是百分比。
`reset()` 同时复位 RTL 和覆盖累计状态。

## 目录及覆盖定义

- `dut/rtl/`：九个上游 RTL 模块及其许可文件。
- `dut/tinyodin_cov_top.v`：顶层封装和覆盖观察信号。
- `dut/coverage_meta.json`：52 个 bin 的名称、条件和固定输出顺序。
- `coverage_simulator.py`、`harness.py`：覆盖累计与六维 action 接口。
- `verilator_harness/`：C++ 逐周期仿真桥及自动编译脚本。
- `examples/smoke_test.py`：独立构建和接口检查。
- `make_mock_recipe.py`：可选的固定 JSON 提案生成工具，用于外部提案编译器开发。

这里的覆盖向量由 Verilator 信号快照及 Python metadata 评估产生。
`dut/covergroup.svh` 是兼容路径占位文件，不包含可供商业仿真器直接执行的完整
SystemVerilog covergroup。内部观察信号供评测器使用，不属于六维刺激输入接口。
此处的 bin 集合用于该评测适配器，不声称覆盖整个处理器的全部验证需求。

## 来源与许可

上游 RTL 的版权和 **Solderpad Hardware License v2.1** 保留在
[`dut/rtl/LICENSE`](dut/rtl/LICENSE)，配套 Apache 2.0 文本为
[`dut/rtl/LICENSE.Apache-2.0`](dut/rtl/LICENSE.Apache-2.0)。
作者、引用要求及文件范围见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
`coverage_simulator.py` 沿用赛方公开 DMA 覆盖评估器的 MIT 许可，版权和完整文本见
[`LICENSES/MIT-EDA-Elite-Challenge.txt`](LICENSES/MIT-EDA-Elite-Challenge.txt)。
其他新增评测适配文件保持原有许可状态，本次发布不额外授予新的开源许可。

本仓库不包含工艺库、综合网表、波形、编译二进制、私有配置或外部项目历史。
