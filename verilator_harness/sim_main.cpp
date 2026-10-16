#include <cstdint>
#include <cstdio>
#include "Vtinyodin_cov_top.h"
#include "verilated.h"

int main(int argc, char **argv) {
    Verilated::commandArgs(argc, argv);
    auto *dut = new Vtinyodin_cov_top;
    dut->clk = 0; dut->rst = 0; dut->sck = 0; dut->mosi = 0;
    dut->aerin_req = 0; dut->aerin_addr = 0; dut->aerout_ack = 0;
    std::printf("rst,sck,mosi,aerin_req,aerin_addr,aerout_ack,aerin_ack,"
                "aerout_req,aerout_addr,sched_full,ctrl_state,spi_cnt,opcode,"
                "prog,read,gate,open,aer_source,max_neur,sq_reset,sq_spi,"
                "sq_aer,sq_spi_aer,sq_hold\n");
    std::fflush(stdout);
    long long rst, sck, mosi, req, addr, out_ack;
    while (std::scanf("%lld %lld %lld %lld %lld %lld",
                      &rst, &sck, &mosi, &req, &addr, &out_ack) == 6) {
        dut->clk = 0; dut->rst = rst & 1; dut->sck = sck & 1;
        dut->mosi = mosi & 1; dut->aerin_req = req & 1;
        dut->aerin_addr = addr & 0x3ff; dut->aerout_ack = out_ack & 1;
        dut->eval(); dut->clk = 1; dut->eval(); dut->clk = 0; dut->eval();
        std::printf("%u,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u,"
                    "%u,%u,%u,%u,%u,%u,%u,%u\n",
            (unsigned)dut->rst, (unsigned)dut->sck, (unsigned)dut->mosi,
            (unsigned)dut->aerin_req, (unsigned)dut->aerin_addr,
            (unsigned)dut->aerout_ack, (unsigned)dut->aerin_ack,
            (unsigned)dut->aerout_req, (unsigned)dut->aerout_addr,
            (unsigned)dut->sched_full, (unsigned)dut->cov_ctrl_state,
            (unsigned)dut->cov_spi_cnt, (unsigned)dut->cov_opcode,
            (unsigned)dut->cov_prog_event, (unsigned)dut->cov_read_event,
            (unsigned)dut->cov_gate_activity, (unsigned)dut->cov_open_loop,
            (unsigned)dut->cov_aer_source, (unsigned)dut->cov_max_neur,
            (unsigned)dut->cov_sq_reset_release,
            (unsigned)dut->cov_sq_spi_program,
            (unsigned)dut->cov_sq_aer_handshake,
            (unsigned)dut->cov_sq_spi_then_aer,
            (unsigned)dut->cov_sq_req_hold);
        std::fflush(stdout);
    }
    dut->final(); delete dut; return 0;
}
